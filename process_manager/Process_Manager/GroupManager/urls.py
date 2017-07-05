# coding:utf-8
from django.conf.urls import include, url

import views as group_views

urlpatterns = [
    url(r'^group_manager/', group_views.index, name='group_manager'),
    url(r'^add_group/', group_views.group_add, name='add_group'),
    url(r'^edit_group/', group_views.group_edit, name='edit_group'),
    url(r'^del_group/', group_views.group_del, name='del_group')
]