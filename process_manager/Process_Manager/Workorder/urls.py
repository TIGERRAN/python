# -*- coding: utf-8 -*-
from django.conf.urls import include, url

import views as wk_views

urlpatterns = [
    url(r'^home/', wk_views.home, name='home'),
    url(r'^apply/', wk_views.order_apply, name='apply_order'),
    url(r'^apply_project/', wk_views.apply_project, name='apply_project'),
    url(r'^apply_project_order/', wk_views.apply_project_order, name='apply_project_order'),
    url(r'^select_sys/', wk_views.select_sys, name='select_sys'),
    url(r'^review/', wk_views.review, name='review'),
    url(r'^downloadFile/', wk_views.download, name='downloadFile')
]