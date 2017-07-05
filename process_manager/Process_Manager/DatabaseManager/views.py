# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .databaseinfo import *
from Login.views import require_role

# Create your views here.
@require_role()
def index(request):
    dt_list = getDBInfo()
    return render(request, 'DatabaseManager/database_manager.html',{'db': dt_list})

@require_role()
def database_add(request):
    DBAs = getDBAUsers()
    if request.method == 'POST':
        db_name = request.POST.get('db_name','')
        db_type = request.POST.get('db_type','')
        host_ip = request.POST.get('host_ip','')
        port = request.POST.get('port','')
        db_manager_id = request.POST.get('db_manager_id','')
        env_id = request.POST.get('env_id','')
        detail = request.POST.get('detail','')
        r = chkDBName(db_name)
        if r:
            addDBInfo(db_name,db_type,host_ip,port,db_manager_id,env_id,detail)
        else:
            return HttpResponse(db_name + u'数据库已经存在')
        return HttpResponseRedirect('/db/database_manager/')
    return render(request, 'DatabaseManager/add_database.html',{'DBAs': DBAs})

@require_role()
def database_edit(request):
    db_id = request.GET['id']
    DBAs = getDBAUsers()
    dt = getDBInfoById(db_id)
    if request.method == 'POST':
        db_type = request.POST.get('db_type','')
        host_ip = request.POST.get('host_ip','')
        port = request.POST.get('port','')
        db_manager_id = request.POST.get('db_manager_id','')
        detail = request.POST.get('detail','')
        env_id = request.POST.get('env_id','')
        setDBInfo(db_id,db_type,host_ip,port,db_manager_id,detail,env_id)
        return HttpResponseRedirect('/db/database_manager/')
    envs=getDBEnv()
    
    return render(request, 'DatabaseManager/edit_database.html', {'db': dt,'DBAs':DBAs,'envs':envs} )

@require_role()
def database_del(request):
    db_id = request.GET.get('id', '')
    delDatabase(db_id)
    dt_list = getDBInfo()
    return HttpResponse('删除成功')