from django.urls import path

from download.views import download_csv, download_csv_streaming, stream_video

urlpatterns = [
    path('download_csv/', download_csv),
    path('download_csv_streaming/', download_csv_streaming),
    path('stream_video/<filename>', stream_video),
]
