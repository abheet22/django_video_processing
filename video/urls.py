from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^uploadvideo/$', views.UploadVideo.as_view(), name='upload_video'),
    url(r'^video-report/$', views.VideoReport.as_view(), name='video_report'),
    url(r'^download-video/$',views.DownloadVideo.as_view(),name='download_video')

]