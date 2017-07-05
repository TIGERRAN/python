# coding:utf-8
from django.conf.urls import include, url

from SystemManager import  views as sys_views

urlpatterns = [
                url(r'^list/', sys_views.index, name='index'),
                url(r'^sys_add/', sys_views.sys_add, name='sys_add'),
                url(r'^sys_edit/', sys_views.sys_edit, name='sys_edit'),
                url(r'^sys_del/', sys_views.sys_del, name='sys_del'),
                url(r'^pj_list/', sys_views.pj_list, name='pj_list'),
                url(r'^pj_add/', sys_views.pj_add, name='pj_add'),
                url(r'^pj_edit/', sys_views.pj_edit, name='pj_edit'),
                url(r'^pj_del/', sys_views.pj_del, name='pj_del'),


]