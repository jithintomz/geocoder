from django.conf.urls import url
from . import views

urlpatterns = [url(r'^$', views.index, name='index'),
url(r'^upload-file/$',views.upload_file,name = "upload_file"),
url(r'^uploads/$',views.uploads,name = "uploads"),
url(r'^download-csv/(?P<uploadid>\d+)/$',views.download_csv,name = "download_csv")
]