# -*- coding: utf-8 -*-
from .models import db_backup_info
from datetime import *
import os, re
import ConfigParser
import time
from DatabaseManager.databaseinfo import getDBInfoById,getDBInfo

def getBackupInfo():
    dbs = db_backup_info.objects.all()
    db_list = list()
    if dbs.count() != 0:
        for db_item in dbs:
            info = getDBInfoById(db_item.db_id)

            if info['env_id'] == 1:
                env = "Online环境"
            elif info['env_id'] == 2:
                env = "Stage环境"
            elif info['env_id'] == 3:
                env = "测试环境"
            else:
                env = "未分配"

            if db_item.is_running == 1:
                status = u'正在进行备份...'
                size = u'正在进行备份...'
                dir = u'正在进行备份...'
            else:
                status,size,dir = log_view(info['db_name'])

            dt = {'id':db_item.id,'name':info['db_name'],'ip':info['host_ip'],'port':info['port'],'env':env,'dir':dir,'size':size,'status':status,'is_running':db_item.is_running}
            db_list.append(dt)
    return db_list

def getDBBackupInfo():
    dbs = db_backup_info.objects.all()
    db_list = list()
    if dbs.count() != 0:
        for db_item in dbs:
            info = getDBInfoById(db_item.db_id)

            if info['env_id'] == 1:
                env = "Online环境"
            elif info['env_id'] == 2:
                env = "Stage环境"
            elif info['env_id'] == 3:
                env = "测试环境"
            else:
                env = "未分配"

            if(db_item.day_of_week == '*'):
                rate = '每一天'
            elif(db_item.day_of_week == 0):
                rate = '每周一'
            elif (db_item.day_of_week == '1'):
                rate = '每周二'
            elif (db_item.day_of_week == '2'):
                rate = '每周三'
            elif (db_item.day_of_week == '3'):
                rate = '每周四'
            elif (db_item.day_of_week == '4'):
                rate = '每周五'
            elif (db_item.day_of_week == '5'):
                rate = '每周六'
            elif (db_item.day_of_week == '6'):
                rate = '每周日'
            strtime = '%s:%s' % (db_item.hour,db_item.minute)
            time = datetime.strptime(strtime, "%H:%M").strftime("%H:%M")

            dt = {'id':db_item.id,'name':info['db_name'],'ip':info['host_ip'],'port':info['port'],'env':env,'rate':rate,'time':time,'status':db_item.status,'is_running':db_item.is_running}
            db_list.append(dt)
    return db_list

def getDBBackupInfoById(id):
    db = db_backup_info.objects.get(id=id)
    strtime = '%s:%s' % (db.hour, db.minute)
    time = datetime.strptime(strtime, "%H:%M").strftime("%H:%M")
    info = getDBInfoById(db.db_id)

    return {'id':db.id,'name':info['db_name'],'ip':info['host_ip'],'port':info['port'],'rate':db.day_of_week,'time':time,'is_running':db.is_running}

def setDBBackupInfoById(id,rate,time):
    timeTuple = datetime.strptime(time, '%H:%M')
    db_backup_info.objects.filter(id=id).update(day_of_week=rate, hour=timeTuple.hour,minute=timeTuple.minute,status=0,is_running=0)

def add_db(db_id,rate,time,shell_file):
    timeTuple = datetime.strptime(time, '%H:%M')
    db = getDBInfoById(db_id)

    baseDir = os.path.dirname(os.path.abspath(__name__))
    sh_dir = os.path.join(baseDir, 'static', 'DBbackup_shell')
    filename = os.path.join(sh_dir, db['db_name'] + '.sh')
    fobj = open(filename, 'wb')
    for chrunk in shell_file.chunks():
        fobj.write(chrunk)
    fobj.close()

    db_backup_info.objects.get_or_create(db_id=db_id,day_of_week=rate, hour=timeTuple.hour,minute=timeTuple.minute,status=0,is_running=0,shell_dir=filename)

def del_db(id):
    db_backup_info.objects.filter(id=id).delete()

def setStatusById(id,status):
    db_backup_info.objects.filter(id=id).update(status=status)

def getStatusById(id):
    db = db_backup_info.objects.get(id=id)
    return db.status

def setRunningById(id,is_running):
    db_backup_info.objects.filter(id=id).update(is_running=is_running)

def getRunningById(id):
    db = db_backup_info.objects.get(id=id)
    return db.is_running

def log_view(db_name):
    time = datetime.now().strftime("%Y%m%d")
    logfile = time + '_' + db_name + ".log"

    baseDir = os.path.dirname(os.path.abspath(__name__))
    log_dir = os.path.join(baseDir, 'static/DBbackup_log', logfile)
    #log_dir = '/tmp/' + logfile
    try:
        fp = open(log_dir, "r")
        content = fp.read()
        status = re.findall('status=(.*)', content)
        size = re.findall('size=(.*)', content)
        dir = re.findall('dir=(.*)', content)
        return status,size,dir
    except:
        status = u'未备份'
        size = u'None'
        dir = u'None'
        return status, size, dir

def getDBlist():
    dblist = getDBInfo()
    return dblist