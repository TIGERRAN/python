# coding:utf-8
from django.conf.urls import include, url

import views as users_views

urlpatterns = [
    url(r'^users_manager/', users_views.index, name='users_manager')
]