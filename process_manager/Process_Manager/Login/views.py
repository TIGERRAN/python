# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .LDAPTools import *
from .forms import LoginForm
from  .userInfo import setUserInfo
from.models import user

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def Login(request):
    form = LoginForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['user']
            password = form.cleaned_data['password']

            #正常登陆
            ret = LDAPLogin(username,password)
            if(ret['result']):
                setUserInfo(ret,request)
                return HttpResponseRedirect('/wk/home/')
            else:
                #return HttpResponse('用户名或密码不正确')
                return render(request, 'Login/login.html', {'message': '用户名或密码不正确'})
    else:
        form = LoginForm()

    return render(request, 'Login/login.html',{'message':''})

def logout(request):
    del request.session['member_id']
    del request.session['member_user']
    del request.session['member_sn']
    del request.session['member_mail']
    del request.session['member_grp']
    return HttpResponseRedirect('/login/')

def require_role():
    def _deco(func):
        def __deco(request, *args, **kwargs):
            try:
                id = request.session['member_id']
                if not id:
                    return HttpResponseRedirect('/login/')
            except:
                return HttpResponseRedirect('/login/')
            return func(request, *args, **kwargs)
        return __deco
    return _deco