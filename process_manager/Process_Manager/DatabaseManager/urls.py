# coding:utf-8
from django.conf.urls import include, url

import views as db_views

urlpatterns = [
    url(r'^database_manager/', db_views.index, name='database_manager'),
    url(r'^add_database/', db_views.database_add, name='add_database'),
    url(r'^edit_database/', db_views.database_edit, name='edit_database'),
    url(r'^del_database/', db_views.database_del, name='del_database'),
]