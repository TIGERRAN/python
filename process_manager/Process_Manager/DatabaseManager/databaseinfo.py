# -*- coding: utf-8 -*-
from .models import db_info,env
from datetime import *
from Login.userInfo import getUserNameById
from Login.models import user

def getDBInfo():
    dbs = db_info.objects.all().order_by("db_name")
    db_list = list()
    if dbs.count() != 0:
        for db_item in dbs:
            time = datetime.strftime(db_item.c_t,"%Y-%m-%d %H:%M:%S")
            manager = getUserNameById(id=db_item.manager_id)
            if db_item.env_id == 1:
                env = "Online环境"
            elif db_item.env_id==2:
                env = "Stage环境"
            elif db_item.env_id==3:
                env = "测试环境"
            else:
                env = "未分配"

            dt = {'db_id':db_item.db_id,'db_name':db_item.db_name,'host_ip':db_item.host_ip,'port':db_item.port,'manager':manager,'env':env,'c_t':time,'detail':db_item.detail}
            db_list.append(dt)
    return db_list

def getDBAUsers():
    users=user.objects.filter(grp_id=666)
    return users

def chkDBName(db_name):
    if db_info.objects.filter(db_name=db_name).exists():
        return False
    return True

def addDBInfo(db_name,db_type,host_ip,port,db_manager_id,env_id,detail):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_info.objects.get_or_create(db_name=db_name,db_type=db_type,host_ip=host_ip,port=port,manager_id=db_manager_id,env_id=env_id,c_t=dt,detail=detail)

def getDBInfoById(db_id):
    db = db_info.objects.get(db_id=db_id)
    env_name=env.objects.get(env_id=db.env_id).env_name
    return {'db_id':db.db_id,'db_name':db.db_name,'db_type':db.db_type,'manager_id':db.manager_id,'env_id':db.env_id,'env_name':env_name,'host_ip':db.host_ip,'port':db.port,'detail':db.detail,'c_t':db.c_t}

def setDBInfo(db_id,db_type,host_ip,port,db_manager_id,detail,env_id):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_info.objects.filter(db_id=db_id).update(db_type=db_type,host_ip=host_ip,port=port,manager_id=db_manager_id,c_t=dt,detail=detail,env_id=env_id)

def delDatabase(db_id):
    db_info.objects.filter(db_id=db_id).delete()
def getDBEnv():
    envs = env.objects.all()
    return envs

def getEnvID(env_name):
    env_id = env.objects.get(env_name=env_name).env_id
    return env_id