# StreamHttpResponse 데모

## 실행
1. django 설치
```sh
pip install django
```

2. 로컬 웹서버 실행
```sh
python manage.py runserver
```

3.데모 실행
```sh
# 비디오 재생 스트리밍 다운로드 방식
http://127.0.0.1:8000/stream_video/test.mp4
# csv 파일 다운로드 스트리밍 방식
http://127.0.0.1:8000/download_csv_streaming/
# csv 파일 다운로드 전체 내용 body에 담는 방식(스트리밍 X)
http://127.0.0.1:8000/download_csv/
```
