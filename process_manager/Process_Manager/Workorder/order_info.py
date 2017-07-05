# -*- coding: utf-8 -*-
from .models import workorder,workorder_sql,workorder_status,workorder_project
from Login.userInfo import getUserNameById,getUserIDByUser,getEmailByGrpID
from datetime import *
from SystemManager.models import sys,project
from DatabaseManager.models import db_info
from django.db.models import Q
import os
from email_api import *
from SystemManager.sys_manager import getPjInfo,Sys_info,get_one_sys,getSysInfo
from operator import itemgetter
from git_api import *
from time import sleep
import threading
from jenkins_api import *

def getOrderInfo(user_id,grp_id):
    #测试
    if(grp_id == 555):
        q_s = Q(status=0)
    #DBA
    elif(grp_id == 666):
        q_s = Q(db_change=1,status=2) | Q(db_change=1,status=7)
    #运维
    elif(grp_id == 777):
        q_s = Q(db_change=0,status=2) | Q(status=3) | Q(status=4) | Q(db_change=0,status=7) | Q(status=8)| Q(status=9)
    #技术经理
    elif(grp_id == 888):
        q_s = Q(status=1)
    #技术总监
    elif(grp_id == 999):
        q_s = Q(status=6)
    else:
        q_s = Q(status=10)
    q_type = Q(order_type=1) | Q(order_type=3)

    if user_id == 1:
        orders = workorder.objects.all()
    else:
        orders = workorder.objects.filter(q_type & (Q(applicant_id=user_id)| Q(status=10) | q_s ))
    orders_p = workorder_project.objects.all()

    order_list = list()
    if orders_p.count() !=0:
        for orders_p_item in orders_p:
            applicant_name = getUserNameById(id=orders_p_item.applicant_id)
            time = datetime.strftime(orders_p_item.c_t,"%Y-%m-%d %H:%M:%S")
            if orders_p_item.status == 0:
                status = "待确认"
            elif orders_p_item.status == 1:
                status = "测试人员已确认"
            elif orders_p_item.status == 2:
                status = "技术经理已确认"
            elif orders_p_item.status == 3:
                status = "stage环境-DBA已确认"
            elif orders_p_item.status == 4:
                status = "stage环境-运维已领取任务"
            elif orders_p_item.status == 5:
                status = "stage环境-运维已确认执行"
            elif orders_p_item.status == 6:
                status = "测试人员已验收"
            elif orders_p_item.status == 7:
                status = "技术总监已确认"
            elif orders_p_item.status == 8:
                status = "online环境-DBA已确认"
            elif orders_p_item.status == 9:
                status = "online环境-运维已领取任务"
            elif orders_p_item.status == 10:
                status = "online环境-运维已确认执行"
            else:
                status = "未知状态"
            order_name = u"项目-" + orders_p_item.order_id

            dt = {'id': orders_p_item.id, 'order_id': orders_p_item.order_id, 'order_name':order_name,'order_type': 5,
                  'pj_id':orders_p_item.pj_ids,'sys_name': '', 'pd_name': '', 'owner_name': '',
                  'applicant_name': applicant_name, 'c_t': time, 'status': status}
            order_list.append(dt)

    if orders.count() != 0:
        for order_item in orders:
            if (order_item.status==4 | order_item.status==9):
                s = workorder_status.objects.get(workorder_id=order_item.id & (Q(status=4) | Q(status=9)))
                if (s.auditor != user_id):
                    continue
            sysinfo = get_one_sys(order_item.sys_id)
            pd_name = getUserNameById(id=sysinfo.pd_id)
            owner_name = getUserNameById(id=sysinfo.owner_id)
            applicant_name = getUserNameById(id=order_item.applicant_id)
            time = datetime.strftime(order_item.c_t,"%Y-%m-%d %H:%M:%S")
            if order_item.status == 0:
                status = "待确认"
            elif order_item.status == 1:
                status = "测试人员已确认"
            elif order_item.status == 2:
                status = "技术经理已确认"
            elif order_item.status == 3:
                status = "stage环境-DBA已确认"
            elif order_item.status == 4:
                status = "stage环境-运维已领取任务"
            elif order_item.status == 5:
                status = "stage环境-运维已确认执行"
            elif orders_p_item.status == 6:
                status = "测试人员已验收"
            elif orders_p_item.status == 7:
                status = "技术总监已确认"
            elif orders_p_item.status == 8:
                status = "online环境-DBA已确认"
            elif orders_p_item.status == 9:
                status = "online环境-运维已领取任务"
            elif orders_p_item.status == 10:
                status = "online环境-运维已确认执行"
            elif orders_p_item.status == 101:
                status = "自动部署失败"
            else:
                status = "未知状态"

            if(order_item.order_type == 1):
                order_name = "BUG-" + order_item.order_id
            elif(order_item.order_type == 3):
                order_name = "DB-" + order_item.order_id

            dt = {'id':order_item.id,'order_id':order_item.order_id,'order_name':order_name,'order_type':order_item.order_type,'pj_id':order_item.pj_id,'sys_name':sysinfo.sys_name,'pd_name':pd_name,'owner_name':owner_name,'applicant_name':applicant_name,'c_t':time,'status':status}
            order_list.append(dt)
    #按时间降序排列
    return sorted(order_list, key=itemgetter('c_t'), reverse=True)

def getApplyInfo(user_id):
    print user_id
    sys_list = list()
    prj_list = list()
    db_list = list()
    sys_info = getSysInfo()
    for sys_item in sys_info:
        prj_info = project.objects.filter(sys_id=sys_item['sys_id'])
        for prj_item in prj_info:
            db = db_info.objects.filter(db_id=prj_item.db_id)
            for db_item in db:
                d_dt = {'db_id': db_item.db_id, 'db_name': db_item.db_name}
                db_list.append(d_dt)
            git_id = getGitProjectIDBySSH(prj_item.git_addr)
            branches = getGitProjectBranchesByID(git_id)
            p_dt = {'pjt_id':prj_item.pjt_id,'project_name':prj_item.project_name,'git_addr':prj_item.git_addr,'branches':branches,'sys_id':prj_item.sys_id}
            print p_dt
            prj_list.append(p_dt)
        s_dt={'sys_id':sys_item['sys_id'],'sys_name':sys_item['sys_name']}
        sys_list.append(s_dt)
    return sys_list,prj_list,db_list

def setWorkorder(order_id,order_type, applicant_id, bug_id, sys_id, pj_id, db_change, db_id, sql_file, conf_change, branch, online_content, effect, online_plan, conf_txt,auto_deploy,url):
    if(order_type == '1'):
        order_name = 'BUG-' + order_id
    elif(order_type == '2'):
        order_name = u'项目-' + order_id
    elif (order_type == '3'):
        order_name = 'DB-' + order_id

    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if(db_change == '1'):
        os.makedirs('static/' + order_name)
        baseDir = os.path.dirname(os.path.abspath(__name__))
        sql_dir = os.path.join(baseDir, 'static', order_name)
        filename = os.path.join(sql_dir, sql_file.name)
        fobj = open(filename, 'wb')
        for chrunk in sql_file.chunks():
            fobj.write(chrunk)
        fobj.close()
    else:
        filename = ''

    workorder.objects.get_or_create(order_type=order_type, bug_id=bug_id, applicant_id=applicant_id, order_id=order_id, sys_id=sys_id, branch=branch,
                                    db_change=db_change, cf_change=conf_change, db_id=db_id, detail=online_content, pj_id=pj_id, online_detail=online_plan, effect_detail=effect, conf_detail=conf_txt, status=0, auto_deploy=auto_deploy,c_t=dt)
    wk = workorder.objects.get(order_type=order_type, bug_id=bug_id, applicant_id=applicant_id, order_id=order_id, sys_id=sys_id, branch=branch,
                               db_change=db_change, cf_change=conf_change, detail=online_content, pj_id=pj_id, online_detail=online_plan, effect_detail=effect, conf_detail=conf_txt, status=0, auto_deploy=auto_deploy, c_t=dt)
    if(db_change == '1'):
        workorder_sql.objects.get_or_create(workorder_id=wk.id,type=order_type,pjt_id=pj_id,db_id=db_id,sql_value=filename,c_t=dt)
        if (order_type == '2'):
            workorder_project.objects.filter(order_id=order_id).update(db_change=1)
    workorder_status.objects.get_or_create(workorder_id=wk.id,type=order_type,pjt_id=pj_id,auditor=applicant_id,status=0,c_t=dt)

    url_parameter = u'id=%s&pj_id=%s&type=%s' % (wk.id,pj_id,order_type)
    url = url + url_parameter
    subject, to, html_content = setSendEmailInfo(order_id, 0, db_change, url)
    send_email(subject, to, html_content)

def getWorkorderInfo(id):
    workorder_info = workorder.objects.get(id=id)
    project_info = project.objects.get(pjt_id=workorder_info.pj_id)
    sys_info = get_one_sys(workorder_info.sys_id)
    owner_name = getUserNameById(id=sys_info.owner_id)
    try:
        sql_info = workorder_sql.objects.get(workorder_id=workorder_info.id)
        db = db_info.objects.get(db_id=sql_info.db_id)
        sql = sql_info.sql_value
        db_name = db.db_name
    except:
        sql = ""
        db_name = ""
    ret = {'id': workorder_info.id, 'type':workorder_info.order_type,'order_id': workorder_info.order_id, 'project_name': project_info.project_name,
           'owner_name': owner_name, 'db_change': workorder_info.db_change,
           'cf_change': workorder_info.cf_change, 'branch': workorder_info.branch, 'detail': workorder_info.detail,
           'effect': workorder_info.effect_detail, 'online_detail': workorder_info.online_detail,
           'conf_datail': workorder_info.conf_detail, 'auto_deploy':workorder_info.auto_deploy,'db_name': db_name, 'sql': sql,'status':workorder_info.status}
    order_status =  workorder_status.objects.filter(workorder_id=workorder_info.id)
    sl = list()
    for status_item in order_status:
        auditorName = getUserNameById(id=status_item.auditor)
        time = datetime.strftime(status_item.c_t,"%Y-%m-%d %H:%M:%S")
        st = {'name':auditorName,'status':status_item.status,'c_t':time}
        sl.append(st)
    return ret,sl

def getSqlFileById(id):
    s = workorder_sql.objects.get(workorder_id=id)
    return s.sql_value

def setSendEmailInfo(order_id,status,db_change,url):
    to = list()
    if status == 0:
        to = getEmailByGrpID(555)
    elif status == '1':
        to = getEmailByGrpID(888)
    elif status == '2':
        if db_change == '1':
            to = getEmailByGrpID(666)
        else:
            to = getEmailByGrpID(777)
    elif status == '3':
        to = getEmailByGrpID(777)
    elif status == '4':
        pass
    elif status == '5':
        to = getEmailByGrpID(555)
    elif status == '6':
        to = getEmailByGrpID(999)
    elif status == '7':
        if db_change == '1':
            to = getEmailByGrpID(666)
        else:
            to = getEmailByGrpID(777)
    elif status == '8':
        to = getEmailByGrpID(777)
    elif status == '9':
        pass
    elif status == '10':
        pass
    else:
        pass
    subject = u'上线申请单:%s' % (order_id)
    html_content = u'<p>有新的上线申请单(%s)需要审核</p><b>链接：</b><a href="%s">%s</a>' % (
        order_id,url,url)

    return subject, to, html_content

def setSendEmailInfoForAutoDeploy(order_id,url,result):
    to = list()
    if result == 'SUCCESS':
        to = getEmailByGrpID(555)
        html_content = u'<p>有新的上线申请单(%s)需要审核</p><b>链接：</b><a href="%s">%s</a>' % (
            order_id, url, url)
    else:
        to = getEmailByGrpID(777)
        html_content = u'<p>上线申请单(%s)自动部署失败</p><b>链接：</b><a href="%s">%s</a>' % (
            order_id, url, url)
    subject = u'上线申请单:%s' % (order_id)

    return subject, to, html_content

def getProjectInfoList():
    dt_list = list()
    Pj_info = getPjInfo()
    for Pj_item in Pj_info:
        sys_infos = Sys_info(Pj_item['sys_id'])
        dt = {'sys_id':Pj_item['sys_id'],'pjt_id':Pj_item['pjt_id'],'sys_name':sys_infos['sys_name'],'pjt_name':Pj_item['project_name'],'owner_name':sys_infos['owner_id'],'pd_name':sys_infos['pd_id']}
        dt_list.append(dt)
    return dt_list

def getOnlineSysName(p_ids):
    if len(p_ids) == 0:
        return []
    name_list = list()
    for p_id in p_ids:
        p = project.objects.get(pjt_id=p_id)
        s = get_one_sys(p.sys_id)
        name_list.append(s.sys_name + "-" + p.project_name)
    return name_list

def setWorkorderProject(applicant_id,ids,s_date,s_time,o_date,o_time):
    time = datetime.now().strftime("%Y%m%d%H%M")
    p_ids = ",".join(ids)
    stage_time = s_date + ' ' + s_time
    online_time = o_date + ' ' + o_time
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    workorder_project.objects.get_or_create(order_id=time,order_type=1,applicant_id=applicant_id,db_change=0,pj_ids=p_ids,stage_time=stage_time,online_time=online_time,status=0,c_t=dt)
    wk = workorder_project.objects.get(order_id=time,order_type=1,applicant_id=applicant_id,db_change=0,pj_ids=p_ids,stage_time=stage_time,online_time=online_time,status=0,c_t=dt)
    workorder_status.objects.get_or_create(workorder_id=wk.id, type=5, pjt_id=p_ids, auditor=applicant_id, status=0,
                                           c_t=dt)

def getWorkorderProjectInfo(id):
    wk_p_info = workorder_project.objects.get(id=id)
    pj_ids = wk_p_info.pj_ids.split(',')
    pj_list = list()
    for p_id in pj_ids:
        project_info = project.objects.get(pjt_id=p_id)
        sys_info = get_one_sys(project_info.sys_id)
        try:
            w_info = workorder.objects.get(order_id=wk_p_info.order_id,pj_id=p_id)
            status_info = workorder_status.objects.filter(workorder_id=w_info.id,type=2,pjt_id=p_id).order_by('-c_t')[0]
            w_id = w_info.id
            status = status_info.status
            if status == 0:
                status_cn = "系统负责人已处理"
            elif status == 1:
                status_cn = "测试人员已确认"
            elif status == 2:
                status_cn = "技术经理已确认"
            elif status == 3:
                status_cn = "stage环境-DBA已确认"
            elif status == 4:
                status_cn = "stage环境-运维已领取任务"
            elif status == 5:
                status_cn = "stage环境-运维已确认执行"
            elif status == 6:
                status_cn = "测试人员已验收"
            elif orders_p_item.status == 7:
                status_cn = "技术总监已确认"
            elif orders_p_item.status == 8:
                status_cn = "online环境-DBA已确认"
            elif orders_p_item.status == 9:
                status_cn = "online环境-运维已领取任务"
            elif orders_p_item.status == 10:
                status_cn = "online环境-运维已确认执行"
        except:
            w_id = 0
            status = -1
            status_cn = u'系统负责人未处理'
        p_dt = {'w_id':w_id,'pj_id':p_id,'sys_name':sys_info.sys_name,'pj_name':project_info.project_name,'status':status,'status_cn':status_cn}
        pj_list.append(p_dt)
    applicant_name = getUserNameById(id=wk_p_info.applicant_id)
    s_time = datetime.strftime(wk_p_info.stage_time,"%Y-%m-%d %H:%M:%S")
    o_time = datetime.strftime(wk_p_info.online_time,"%Y-%m-%d %H:%M:%S")
    dt = {'order_id':wk_p_info.order_id,'stage_time':s_time,'online_time':o_time,'applicant_name':applicant_name,'db_change':wk_p_info.db_change,'pj_count':len(pj_list),'status':wk_p_info.status,'pj_info':pj_list}

    order_status =  workorder_status.objects.filter(workorder_id=id,type=5)
    sl = list()
    for status_item in order_status:
        auditorName = getUserNameById(id=status_item.auditor)
        time = datetime.strftime(status_item.c_t,"%Y-%m-%d %H:%M:%S")
        st = {'name':auditorName,'status':status_item.status,'c_t':time}
        sl.append(st)

    return dt,sl

def getProjectOrderInfo(p_id):
    p_info = project.objects.get(pjt_id=p_id)
    s_info = get_one_sys(p_info.sys_id)
    git_id = getGitProjectIDBySSH(p_info.git_addr)
    branches = getGitProjectBranchesByID(git_id)
    dt = {'sys_id':p_info.sys_id,'sys_name':s_info.sys_name,'project_name':p_info.project_name,'project_git':p_info.git_addr,'branches':branches}

    db_list = list()
    db = db_info.objects.filter(db_id=p_info.db_id)
    for db_item in db:
        d_dt = {'db_id': db_item.db_id, 'db_name': db_item.db_name}
        db_list.append(d_dt)

    return dt,db_list

def deploy(id,type,pj_id,status,user_id,url):
    if(type == '1' and status == 2 ):
        o = workorder.objects.get(id=id)
        if (o.auto_deploy > 0):
            t = threading.Thread(target=auto_deploy, args=[id,type,pj_id,status,user_id,url,o.auto_deploy])
            t.setDaemon(True)
            t.start()

def updateWorkorderStatus(id, type, pj_id, status, user_id, url):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if (type == '5'):
        o = workorder_project.objects.get(id=id)
        if (status == 2 and o.db_change == 0):
            status = 4
        if (status == 7 and o.db_change == 0):
            status = 9
        workorder_project.objects.filter(id=id).update(status=status, u_t=dt)
    else:
        o = workorder.objects.get(id=id)
        if (status == 2 and o.db_change == 0):
            status = 4
        if (status == 7 and o.db_change == 0):
            status = 9
    workorder.objects.filter(id=id).update(status=status, u_t=dt)
    workorder_status.objects.get_or_create(workorder_id=id, type=type, pjt_id=pj_id, auditor=user_id, status=status,
                                               c_t=dt)
    subject, to, html_content = setSendEmailInfo(o.order_id, status, o.db_change, url)
    send_email(subject, to, html_content)

def auto_deploy(id, type, pj_id, status, user_id, url,time):
    sleep_time = time * 60
    sleep(sleep_time)

    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    o = workorder.objects.get(id=id)
    branch = o.branch
    p = project.objects.get(pjt_id=o.pj_id)
    p_name = p.project_name
    jenkins_name = 'cd-stage-' + p_name.replace('_','-')

    result =  BuildJob(jenkins_name,branch)
    if result == 'SUCCESS':
        status = status + 3
    else:
        status = 101
    workorder.objects.filter(id=id).update(status=status, u_t=dt)
    workorder_status.objects.get_or_create(workorder_id=id, type=type, pjt_id=pj_id, auditor=user_id, status=status,
                                           c_t=dt)
    setSendEmailInfoForAutoDeploy(o.order_id,url,result)
    subject, to, html_content = setSendEmailInfoForAutoDeploy(o.order_id, url, result)
    send_email(subject, to, html_content)