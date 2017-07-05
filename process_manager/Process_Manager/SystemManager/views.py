# -*- coding: utf-8 -*-
from django.shortcuts import render
from sys_manager import *
# import sys_manager
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from DatabaseManager.databaseinfo import getDBInfo
from Login.views import require_role

# Create your views here.
@require_role()
def index(request):
    syslist = GetSys()
    if syslist != 0:
        # return HttpResponse(syslist)
        return render(request, 'sys/index.html',{'sys_list': syslist})
    else:
        return HttpResponse('信息不正确')
        return render(request,'sys/index.html')

@require_role()
def sys_add(request):

    if request.method == 'POST':
        form = Addsys(request.POST)
        if form.is_valid() is True:
            sys_name= form.cleaned_data['sys_name']
            owner_id= form.cleaned_data['owner_id']
            pd_id = form.cleaned_data['pd_id']

            SetSys(sys_name, owner_id, pd_id)

            syslist = getSysInfo()

            return render(request, 'sys/index.html',{'sys_list':syslist})
        else:
            return HttpResponse('信息不正确')

    user_all = get_user_all()
    return render(request, 'sys/add.html',{'users':user_all})

@require_role()
def sys_edit(request):

    if request.method == 'POST':
        form = set_sys(request.POST)
        if form.is_valid() is True:
            sys_id = form.cleaned_data['sys_id']
            sys_name = form.cleaned_data['sys_name']
            owner_id = form.cleaned_data['owner_id']
            if owner_id == 0:
                owner_id=get_one_sys(sys_id).owner_id
            pd_id = form.cleaned_data['pd_id']
            if pd_id == 0:
                pd_id = get_one_sys(sys_id).pd_id
            DA={'sys_id':sys_id,'sys_name':sys_name,'owner_id':owner_id,'pd_id':pd_id}
            # print
            update_sys(sys_id,sys_name,owner_id,pd_id)
            return HttpResponseRedirect('/sys/list/')
            # syslist = getSysInfo()
            # return render(request, 'sys/index.html', {'sys_list': syslist})
    if request.method == 'GET':
        sys_id = request.GET.get('sys_id', '')
        if sys_id:
            sys_info = Sys_info(sys_id)
            #用户组 1004 为开发人员用户组
            user_all = get_user_by_grp_id(1004)
            # print user_all
            return render(request, 'sys/sysedit.html', {'sysinfo': sys_info,'users':user_all})
    # else:
    #     syslist = getSysInfo()
    #     return render(request, 'sys/index.html', {'sys_list': syslist})

@require_role()
def pj_list(request):
    project_list= GetProjects()

    if project_list != 0:
        return render(request, 'sys/pj_list.html',{'pj_list': project_list})
    else:
        return render(request,'sys/index.html')

@require_role()
def pj_add(request):

    if request.method == 'POST':
        form = Add_pj_form(request.POST)
        if form.is_valid() is True:
            sys_id          = form.cleaned_data['sys_id']
            project_name    = form.cleaned_data['project_name']
            git_addr        = form.cleaned_data['git_addr']
            db_id           = form.cleaned_data['db_id']

            SetProject(sys_id,project_name,git_addr,db_id)

            return HttpResponseRedirect('/sys/pj_list/')

        else:
            return HttpResponse('信息不正确')


        project_list= GetProjects()
        return render(request, 'sys/pj_list.html',{'pj_list': project_list})

    else:

        sys_info = getSysInfo()
        db_info = getDBInfo()
        return render(request,'sys/pj_add.html',{'sysinfo': sys_info,'db_info':db_info})

@require_role()
def  pj_edit(request):

    if request.method == 'GET':
        pjt_id = request.GET.get('pjt_id', '')
        if pjt_id:
            # print user_all
            pj_info=Get_Project_One(pjt_id)
            sys_info = getSysInfo()
            db_info = getDBInfo()
            return render(request, 'sys/pj_edit.html', {'pj_info': pj_info,'sys_info':sys_info,'db_info':db_info})

    if request.method == 'POST':
        form = Up_pj_form(request.POST)
        if form.is_valid() is True:
            pjt_id          = form.cleaned_data['pjt_id']
            sys_id          = form.cleaned_data['sys_id']
            project_name    = form.cleaned_data['project_name']
            git_addr        = form.cleaned_data['git_addr']
            db_id           = form.cleaned_data['db_id']
            # if db_id == 0:
            #     db_id = project.objects.get(pjt_id=pjt_id).db_id
            if sys_id == 0:
                sys_id = project.objects.get(pjt_id=pjt_id).sys_id

            Update_Project(pjt_id,project_name,sys_id,git_addr,db_id)
        else:
            return HttpResponse('信息不正确')
        project_list= GetProjects()
        return render(request, 'sys/pj_list.html',{'pj_list': project_list})

@require_role()
def pj_del(request):

    if request.method == 'GET':
        pjt_id = request.GET.get('pjt_id', '')
        delProject(pjt_id)
        project_list= GetProjects()
        return render(request, 'sys/pj_list.html',{'pj_list': project_list})

@require_role()
def sys_del(request):
    if request.method == 'GET':
        sys_id = request.GET.get('sys_id', '')
        delSys(sys_id)
        syslist = GetSys()

        # return HttpResponse(syslist)
        return render(request, 'sys/index.html',{'sys_list': syslist})

        