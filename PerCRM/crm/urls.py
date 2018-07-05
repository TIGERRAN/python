# -*- coding: utf-8 -*-

from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sale/$', views.sale, name='sale'),
    url(r'^student/$', views.student, name='student'),
    url(r'^teacher/$', views.teacher, name='teacher'),
]
