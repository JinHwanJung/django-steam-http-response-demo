import csv
import mimetypes
import os
import re
from io import StringIO

from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse


def big_csv(num_row):
    for row in range(num_row):
        output = StringIO()
        writer = csv.writer(output)
        if row == 0:
            writer.writerow(['row'])
        else:
            writer.writerow([row])
        output.seek(0)
        yield output.read()


class FileWrapper(object):
    def __init__(self, path, chunk_bytes=8192, offset=0, length=None):
        self.file = open(path, 'rb')
        print(self.file)
        self.file.seek(offset, os.SEEK_SET)
        self.chunk_bytes = chunk_bytes
        self.length = length

    def __iter__(self):
        return self

    def __next__(self):
        if self.length is None:
            data = self.file.read()
            if data:
                return data
            raise StopIteration()
        else:
            if self.length <= 0:
                raise StopIteration()
            data = self.file.read(min(self.length, self.chunk_bytes))
            if not data:
                raise StopIteration()
            self.length -= len(data)
            return data


def download_csv(request):
    csv_file = "".join(big_csv(1_000_000))
    response = HttpResponse(csv_file, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=big.csv'
    response['Content-Length'] = len(csv_file)
    return response


def download_csv_streaming(request):
    response = StreamingHttpResponse(big_csv(1_000_000), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=big.csv'
    return response


def stream_video(request, filename):
    path = "".join((settings.BASE_DIR, '/static/', filename))
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    # content_type: https://developer.mozilla.org/ko/docs/Web/HTTP/Basics_of_HTTP/MIME_types 참고
    content_type = content_type or 'application/octet-stream'

    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size -1
        length = last_byte - first_byte + 1
        # 206 Partial Content: https://developer.mozilla.org/ko/docs/Web/HTTP/Status/206
        response = StreamingHttpResponse(FileWrapper(
            path, offset=first_byte, length=length), status=206, content_type=content_type)
        response['Content-Length'] = str(size)
        response['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        response = StreamingHttpResponse(FileWrapper(path), content_type=content_type)
        response['Content-Length'] = str(size)
    response['Accept-Ranges'] = 'bytes'
    return response
