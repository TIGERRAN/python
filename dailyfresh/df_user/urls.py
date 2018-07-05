from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='registry'),
    url(r'^register_handle/$', views.register_handle, name='register_handle'),
    url(r'^check_exist', views.check_exist, name='check_exist'),
    url(r'login/$', views.login, name='login'),
    url(r'^login_handle/$', views.login_handle, name='login_handle'),
    url(r'^info/$', views.userCenter_info, name='userCenter_info'),
    url(r'^order/$', views.userCenter_order, name='userCenter_order'),
    url(r'site/$', views.userCenter_site, name='userCenter_site'),
    url(r'site_handle/$', views.site_handle, name='site_handle'),
    url(r'^logout/$', views.logout, name='logout'),
]
