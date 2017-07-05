"""Process_Manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from Login import views as login_views
#from Workorder import views as work_views
import Login.urls
import SystemManager.urls
import GroupManager.urls
import DatabaseManager.urls
import Workorder.urls
import UsersManager.urls
import DatabaseBackup.urls

urlpatterns = [
    url(r'^$', login_views.Login, name='login'),
    url(r'^login/', include(Login.urls)),
    url(r'^grp/', include(GroupManager.urls)),
    url(r'^db/', include(DatabaseManager.urls)),
    url(r'^wk/', include(Workorder.urls)),
    url(r'^user/', include(UsersManager.urls)),
    url(r'^db_backup/', include(DatabaseBackup.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^sys/',include(SystemManager.urls))
]
