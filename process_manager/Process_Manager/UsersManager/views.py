# -*- coding: utf-8 -*-
from django.shortcuts import render
from .usersinfo import getUsersInfo
from django.http import HttpResponseRedirect,HttpResponse
from Login.views import require_role

# Create your views here.
@require_role()
def index(request):
    dt_list = getUsersInfo()
    return render(request, 'UsersManager/users_manager.html',{'users': dt_list})