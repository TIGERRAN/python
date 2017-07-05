# coding:utf-8
from django.conf.urls import include, url

import views as db_views

urlpatterns = [
    url(r'^db_backup_view/', db_views.index, name='db_backup_view'),
    url(r'^db_backup_manager/', db_views.db_manager, name='db_backup_manager'),
    url(r'^add_db/', db_views.db_add, name='add_db'),
    url(r'^edit_db/', db_views.db_edit, name='edit_db'),
    url(r'^del_db/', db_views.db_del, name='del_db'),
]