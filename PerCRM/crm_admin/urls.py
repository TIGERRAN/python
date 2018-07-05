# -*- coding: utf-8 -*-

from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(\w+)/$', views.handle_models, name='hanle_models'),
    url(r'^(\w+)/(\w+)/$', views.handle_tables, name='hanle_tables'),
    url(r'^(\w+)/(\w+)/(\w+)/change/$', views.change_tables, name='change_tables'),
]
