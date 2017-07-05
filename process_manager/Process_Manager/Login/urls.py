# -*- coding: utf-8 -*-
from django.conf.urls import include, url

import views as login_views

urlpatterns = [
    url(r'^$', login_views.Login, name='login'),
    url(r'^logout/', login_views.logout, name='logout'),
]