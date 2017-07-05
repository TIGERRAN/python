# -*- coding: utf-8 -*-
from Login.models import user
from GroupManager.groupinfo import getGroupNameById
from operator import itemgetter
from datetime import *

def getUsersInfo():
    users_list = user.objects.all()
    dt_list = list()
    if users_list.count() != 0:
        for user_item in users_list:
            grp_name = getGroupNameById(user_item.grp_id)
            time = datetime.strftime(user_item.c_t, "%Y-%m-%d %H:%M:%S")
            dt = {'id':user_item.id,'user':user_item.user,'name':user_item.username,'email':user_item.email,'group':grp_name,'c_t':time}
            dt_list.append(dt)
    return sorted(dt_list, key=itemgetter('id'))

def getUsersByGrpId(grp_id):
    users_list = user.objects.filter(grp_id=grp_id)
    dt_list = list()
    if users_list.count() != 0:
        for user_item in users_list:
            grp_name = getGroupNameById(user_item.grp_id)
            time = datetime.strftime(user_item.c_t, "%Y-%m-%d %H:%M:%S")
            dt = {'id':user_item.id,'user':user_item.user,'name':user_item.username,'email':user_item.email,'group':grp_name,'c_t':time}
            dt_list.append(dt)
    return sorted(dt_list, key=itemgetter('id'))