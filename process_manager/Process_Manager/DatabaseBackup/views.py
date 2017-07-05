# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .db_backup_info import *
from .backupThread import *
from Login.views import require_role

# Create your views here.
@require_role()
def index(request):
    dt_list = getBackupInfo()
    if request.method == 'POST':
        id = request.POST.get('backup', '')
        ret = M_backup(id)
        if ret == False:
            return HttpResponse(u'shell文件不存在')
        setRunningById(id,1)
        return HttpResponseRedirect('/db_backup/db_backup_view/')
    return render(request, 'DatabaseBackup/db_backup_view.html', {'db': dt_list})

@require_role()
def db_manager(request):
    dt_list = getDBBackupInfo()
    if request.method == 'POST':
        en_id = request.POST.get('enable', '')
        if en_id:
            ret = startAutoBackup(en_id)
            if ret == False:
                return HttpResponse(u'shell文件不存在')
        dis_id = request.POST.get('disable', '')
        if dis_id:
            stopAutoBackup(dis_id)
        return HttpResponseRedirect('/db_backup/db_backup_manager/')
    return render(request, 'DatabaseBackup/db_backup_manager.html', {'db': dt_list})

@require_role()
def db_add(request):
    db_list = getDBlist()
    if request.method == 'POST':
        db_id = request.POST.get('db_id', '*')
        rate = request.POST.get('rate', '*')
        time = request.POST.get('time', '02:00')
        shell_file = request.FILES.get('shell_file', '')

        add_db(db_id, rate, time, shell_file)
        return HttpResponseRedirect('/db_backup/db_backup_manager/')
    return render(request, 'DatabaseBackup/add_db.html',{'db_list':db_list})

@require_role()
def db_edit(request):
    id = request.GET['id']
    dt = getDBBackupInfoById(id)
    if request.method == 'POST':
        rate = request.POST.get('rate', '*')
        time = request.POST.get('time', '02:00')
        setDBBackupInfoById(id, rate, time)
        return HttpResponseRedirect('/db_backup/db_backup_manager/')
    return render(request, 'DatabaseBackup/edit_db.html', {'db': dt})

@require_role()
def db_del(request):
    id = request.GET.get('id', '')
    del_db(id)
    return HttpResponse(u'删除成功')