from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^handle_order/$', views.handle_order, name='handle_order'),
]
