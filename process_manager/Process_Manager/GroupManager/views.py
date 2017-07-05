# -*- coding: utf-8 -*-
from django.shortcuts import render

from UsersManager import usersinfo
from .groupinfo import getGroupsInfo,addGroupItem,getGroupMembersById,setGroupItem,delGroup
from django.http import HttpResponseRedirect,HttpResponse
from Login.views import require_role

# Create your views here.
@require_role()
def index(request):
    dt_list = getGroupsInfo()
    return render(request, 'GroupManager/group_manager.html',{'group': dt_list})

@require_role()
def group_add(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        enable = request.POST.get('enable','')
        detail = request.POST.get('detail','')
        addGroupItem(name,enable,detail)
        return HttpResponseRedirect('/grp/group_manager/')
    return render(request, 'GroupManager/add_group.html')

@require_role()
def group_edit(request):
    grp_id = request.GET.get('id','')
    dt = getGroupMembersById(grp_id)
    if request.method == 'POST':
        name = request.POST.get('grp_name', '')
        members = request.POST.getlist('members', '')
        detail = request.POST.get('detail', '')
        setGroupItem(grp_id,members,detail)
        return HttpResponseRedirect('/grp/group_manager/')
    this_grp_users = usersinfo.getUsersByGrpId(grp_id)
    unknown_grp_users = usersinfo.getUsersByGrpId(0)
    return render(request, 'GroupManager/edit_group.html', {'group': dt, 'thisGrpUsers': this_grp_users, 'unkownGrpUsers': unknown_grp_users})

@require_role()
def group_del(request):
    group_id = request.GET.get('id', '')
    delGroup(group_id)
    return HttpResponse('删除成功')