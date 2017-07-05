# -*- coding: utf-8 -*-
from .models import sys,project
from datetime import *
from Login.models import user
from DatabaseManager.models import *
# from Login.models import user

def getSysInfo():
    sys_list = sys.objects.all()
    dt_list = list()
    if sys_list.count() != 0:
        for sys_item in sys_list:
            dt = {'sys_id':sys_item.sys_id,'sys_name':sys_item.sys_name,'owner_id':sys_item.owner_id,'pd_id':sys_item.pd_id}
            dt_list.append(dt)

        return dt_list

    else:
        return 0

class info():
    sys_info={
        'sys_name': '',
        'owner_id':'',
        'pd_id': ''

    }

def SetSys(sys_name,owner_id,pd_id):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #查找用户记录
    o = sys.objects.filter(sys_name=sys_name)
    if(o.count() == 0):
        sys.objects.get_or_create(sys_name=sys_name, owner_id=owner_id,
                                pd_id=pd_id, c_t=dt)

def SetProject(sys_id,project_name,git_addr,db_id):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    o = project.objects.filter(project_name=project_name)
    if(o.count()==0):
        project.objects.get_or_create(sys_id=sys_id,project_name=project_name,
                                    git_addr=git_addr, db_id=db_id, c_t=dt)

def Sys_info(sys_id):
    # print type(sys_id)
    sys_info=sys.objects.get(sys_id=sys_id)
    sys_owner=user.objects.get(id=sys_info.owner_id)
    sys_pd=user.objects.get(id=sys_info.pd_id)
    sys_dt={'sys_id':sys_info.sys_id,'sys_name':sys_info.sys_name,'owner_id':sys_owner.username,'pd_id':sys_pd.username}

    return sys_dt

def get_user_all():
    user_list = user.objects.all()
    dt_list=list()

    for user_item in user_list:
        dt = {'user_id':user_item.id,'user_name':user_item.username}
        dt_list.append(dt)
    return dt_list
def get_user_by_grp_id(grp_id):
    user_list = user.objects.filter(grp_id=grp_id)
    dt_list = list()
    for user_item in user_list:
        dt = {'user_id':user_item.id,'user_name':user_item.username}
        dt_list.append(dt)
    return dt_list

def get_one_sys(sys_id):
    BA = sys.objects.get(sys_id=sys_id)
    return BA


def update_sys(sys_id,sys_name,owner_id,pd_id):

    sys.objects.filter(sys_id=sys_id).update(sys_name=sys_name, owner_id=owner_id, pd_id=pd_id)

def getPjInfo():
    project_list = project.objects.all()
    dt_list = list()
    if project_list.count() != 0:
        for project_item in project_list:
            dt = {'pjt_id':project_item.pjt_id,'sys_id':project_item.sys_id,'project_name':project_item.project_name}
            dt_list.append(dt)
        return dt_list
    else:
        return 0

def GetUserName(uid):
    user_name = user.objects.get(id=uid).username
    return user_name


def GetSys():
    sys_list = sys.objects.all()
    dt_list = list()
    if sys_list.count() != 0:
        for sys_item in sys_list:
            owner_name= GetUserName(sys_item.owner_id)
            pd_name =  GetUserName(sys_item.pd_id)
            dt = {'sys_id':sys_item.sys_id,'sys_name':sys_item.sys_name,'owner_id':owner_name,'pd_id':pd_name}
            dt_list.append(dt)

        return dt_list

    else:
        return 0
def delSys(sys_id):
    sys.objects.filter(sys_id=sys_id).delete()

def GetProjects():
    pj_list = project.objects.all()
    dt_list = list()
    # if pj_list.count() != 0:
    num=1
    for pj_item in  pj_list:
        sys_name = sys.objects.get(sys_id=pj_item.sys_id).sys_name
        
        # db_name = db_info.objects.get(db_id=pj_item.db_id).db_name
        if pj_item.db_id == 0:
            db_name = "无关联数据库"
        else:
            db = db_info.objects.filter(db_id=pj_item.db_id)
            if db.count()==0:
                db_name = '无关联数据库'
            else:
                db_name= db[0].db_name

        c_t=datetime.strftime(pj_item.c_t,"%Y-%m-%d %H:%M:%S")

        dt={'num':num,'pjt_id':pj_item.pjt_id,'sys_name':sys_name,'project_name':pj_item.project_name,'git_addr':pj_item.git_addr,'db_name':db_name,'c_t':c_t}
        num =num + 1
        dt_list.append(dt)
    # print dt_list
    return dt_list

    # else:
    #     return 0

def Get_Project_One(pjt_id):
    pj_item =project.objects.get(pjt_id=pjt_id)
    sys_name = sys.objects.get(sys_id=pj_item.sys_id).sys_name
    if pj_item.db_id == 0:
        db_name = "无数据库关联"
    else:
        db = db_info.objects.filter(db_id=pj_item.db_id)
        if db.count()==0:
            db_name = '无关联数据库'
        else:
            db_name= db[0].db_name

    c_t = datetime.strftime(pj_item.c_t, "%Y-%m-%d %H:%M:%S")
    return {'pjt_id':pj_item.pjt_id,'sys_name':sys_name,'project_name':pj_item.project_name,'git_addr':pj_item.git_addr,'db_id':pj_item.db_id,'db_name':db_name,'c_t':c_t}

def Update_Project(pjt_id,project_name,sys_id,git_addr,db_id):
    # o = project.objects.filter(project_name=project_name)
    # if(o.count() == 0):
    project.objects.filter(pjt_id=pjt_id).update(project_name=project_name, sys_id=sys_id, git_addr=git_addr,db_id=db_id)

def delProject(pjt_id):
    project.objects.filter(pjt_id=pjt_id).delete()


