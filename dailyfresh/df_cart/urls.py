from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.cart, name='cart'),
    url(r'^getinfo/$', views.getinfo, name='getinfo'),
    url(r'^add/$', views.add, name='add'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^delete/$', views.delete, name='delete'),
]
