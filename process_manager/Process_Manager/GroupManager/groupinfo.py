# -*- coding: utf-8 -*-
from .models import group
from Login.models import user
from datetime import *

'''
555 测试人员
666 DBA
777 运维人员
888 技术经理
999 技术总监
'''


def getGroupsInfo():
    grp_list = group.objects.all()
    dt_list = list()
    if grp_list.count() != 0:
        for grp_item in grp_list:
            grp_memebers = user.objects.filter(grp_id=grp_item.grp_id)
            members = ''
            member_list = list()
            for member_item in grp_memebers:
                member_list.append(member_item.username)
            members = ','.join(member_list)
            dt = {'id':grp_item.grp_id,'name':grp_item.grp_name,'members':members,'detail':grp_item.detail}
            dt_list.append(dt)
    return dt_list

def addGroupItem(name,enable,detail):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    group.objects.get_or_create(grp_name=name,detail=detail,c_t=dt)

def getGroupMembersById(id):
    grp_info = group.objects.get(grp_id=id)
    grp_members = user.objects.filter(grp_id=id)
    member_list = list()
    for member in grp_members:
        member_list.append(member.user)
    str_member = ','.join(member_list)

    return {'grp_id':grp_info.grp_id,'grp_name':grp_info.grp_name,'members':str_member,'detail':grp_info.detail}

def setGroupItem(grp_id,members,detail):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    group.objects.filter(grp_id=grp_id).update(detail=detail,c_t=dt)
    user.objects.filter(grp_id=grp_id).update(grp_id=0)
    for member in  members:
        user.objects.filter(user=member).update(grp_id=grp_id)

def delGroup(grp_id):
    group.objects.filter(grp_id=grp_id).delete()
    user.objects.filter(grp_id=grp_id).update(grp_id=999)

def getGroupNameById(id):
    grp_info = group.objects.get(grp_id=id)
    return grp_info.grp_name
