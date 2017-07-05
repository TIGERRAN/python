# -*- coding: utf-8 -*-
from .models import user
from datetime import *

def setUserInfo(user_info,request):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #查找用户记录
    o = user.objects.filter(user=user_info['uid'])
    if(o.count() == 0):
           # 没查到
        user.objects.get_or_create(user=user_info['uid'], username=user_info['sn'],
                                       email=user_info['mail'], grp_id=0, c_t=dt)
    else:
        user.objects.filter(user=user_info['uid']).update(c_t=dt)

    m = user.objects.get(user=user_info['uid'])
    request.session['member_id'] = m.id
    request.session['member_user'] = m.user
    request.session['member_sn'] = m.username
    request.session['member_mail'] = m.email
    request.session['member_grp'] = m.grp_id

def getUserNameById(id):
    o = user.objects.get(id=id)
    return o.username

def getUserIDByUser(user):
    o = user.objects.get(user=user)
    return o.id

def getEmailByGrpID(grp_id):
    u = user.objects.filter(grp_id=grp_id)
    email_list = list()
    for u_item in u:
        email_list.append(u_item.email)
    return  email_list