from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'site_handle/$', views.site_handle, name='site_handle'),
    url(r'^$', views.index, name='index'),
    url(r'^list/$', views.list, name='list'),
    url(r'^([1-9][0-9]*)/$', views.detail, name='detail'),
]
