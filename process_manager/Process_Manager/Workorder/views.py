# -*- coding: utf-8 -*-
from django.shortcuts import render
from .order_info import *
from django.http import HttpResponseRedirect,HttpResponse,StreamingHttpResponse,response
from Login.views import require_role
import json
from django.core.urlresolvers import reverse

# Create your views here.

@require_role()
def home(request):
    orders = getOrderInfo(request.session['member_id'],request.session['member_grp'])
    user_dt={'id':request.session['member_id'],'sn':request.session['member_sn']}
    return render(request, 'Workorder/home.html',{'orders':orders,'user':user_dt})

@require_role()
def order_apply(request):
    ds,dp,dd = getApplyInfo(request.session['member_id']) # 创建系统上线申请单
    if request.method == 'POST':   #上线申请单提交
        type = request.POST.get('type', '')
        time = datetime.now().strftime("%Y%m%d%H%M")
        url = 'http://' + request.META['HTTP_HOST'] + '/wk/review/?'
        if(type == '1'):
            bug_id = request.POST.get('bug_id', 0)
            if bug_id == '':
                bug_id = 0
            bug_sys_id = request.POST.get('bug_sys_name', 0)
            bug_pj_id = request.POST.get('bug_pj_name', 0)
            bug_db_change = request.POST.get('bug_db_change', 0)
            bug_db_id = request.POST.get('bug_db_name', 0)
            bug_sql = request.FILES.get('bug_sql','')
            if (len(bug_sql) == 0 and bug_db_change == '1'):
                return HttpResponse('error')
            bug_conf_change = request.POST.get('bug_conf_change', '')
            bug_branch = request.POST.get('bug_branch', '')
            bug_online_content = request.POST.get('bug_online_content', '')
            bug_effect = request.POST.get('bug_effect', '')
            bug_online_plan = request.POST.get('bug_online_plan', '')
            bug_conf_txt = request.POST.get('bug_conf_txt', '')
            if(bug_db_change == '0'):
                auto_deploy = request.POST.get('auto_deploy', 0)
            else:
                auto_deploy = 0
            applicant_id = request.session['member_id']
            setWorkorder(time,type,applicant_id,bug_id,bug_sys_id,bug_pj_id,bug_db_change,bug_db_id,bug_sql,bug_conf_change,bug_branch,bug_online_content,bug_effect,bug_online_plan,bug_conf_txt,auto_deploy,url)
        elif (type == '3'):
            db_apply_sys_id = request.POST.get('db_apply_sys_name', '')
            db_apply_pj_id = request.POST.get('db_apply_pj_name', '')
            db_apply_db_id = request.POST.get('db_apply_db_id', '')
            db_apply_sql = request.FILES.get('db_apply_sql', '')
            if (len(db_apply_sql) == 0):
                return HttpResponse('error')
            db_apply_detail = request.POST.get('db_apply_detail', '')
            applicant_id = request.session['member_id']
            setWorkorder(time,type,applicant_id,0,db_apply_sys_id,db_apply_pj_id,'1',db_apply_db_id,db_apply_sql,0,'',db_apply_detail,'','','',0,url)
        return HttpResponseRedirect('/wk/home/')
    return render(request, 'Workorder/apply_order.html',{'sys_info':ds,'prj_info':dp,'db_info':dd})

@require_role()
def apply_project(request):
    p_id = request.GET.getlist('id',[])
    nameList = getOnlineSysName(p_id)
    if request.method == 'POST':
        stage_date = request.POST.get('stage_date', '')
        stage_time = request.POST.get('stage_time', '')
        online_date = request.POST.get('online_date', '')
        online_time = request.POST.get('online_time', '')
        applicant_id = request.session['member_id']
        setWorkorderProject(applicant_id,p_id,stage_date,stage_time,online_date,online_time)

        return HttpResponseRedirect('/wk/home/')
    return render(request, 'Workorder/apply_project.html',{'sys':nameList})

def apply_project_order(request):
    order_id = request.GET.get('order','')
    pj_id = request.GET.get('id','')
    dt,db = getProjectOrderInfo(pj_id)
    url = 'http://' + request.META['HTTP_HOST'] + '/wk/review/?'

    if request.method == 'POST':
        sys_id = dt['sys_id']
        db_change = request.POST.get('db_change', 0)
        db_id = request.POST.get('db_name', 0)
        sql = request.FILES.get('sql', '')
        if (len(sql) == 0 and db_change == 1):
            return HttpResponse('error')
        conf_change = request.POST.get('conf_change', '')
        branch = request.POST.get('branch', '')
        online_content = request.POST.get('online_content', '')
        effect = request.POST.get('effect', '')
        online_plan = request.POST.get('online_plan', '')
        conf_txt = request.POST.get('conf_txt', '')
        if (db_change == '0'):
            auto_deploy = request.POST.get('auto_deploy', 0)
        else:
            auto_deploy = 0
        applicant_id = request.session['member_id']
        setWorkorder(order_id,'2', applicant_id, 0, sys_id, pj_id, db_change, db_id, sql,
                     conf_change, branch, online_content, effect, online_plan, conf_txt,auto_deploy,url)
        return HttpResponseRedirect('/wk/home/')

    return render(request, 'Workorder/apply_project_order.html',{'pj_info':dt,'db_info':db,'order_name':order_id})

@require_role()
def select_sys(request):
    pj_info = getProjectInfoList()
    if request.method == 'POST':
        id_list = request.POST.getlist('pj_id', [])
        str_list = list()
        for id_item in id_list:
            str='id=' + id_item
            str_list.append(str)
        attr = "&".join(str_list)
        return HttpResponseRedirect('/wk/apply_project/?'+attr)
    return render(request, 'Workorder/select_sys.html',{'pj_info':pj_info})

@require_role()
def review(request):
    id = request.GET['id']
    pj_id = request.GET['pj_id']
    type = request.GET['type']

    if request.method == 'POST':
        status_value = request.POST.get('confirm', '')
        url = request.META['HTTP_REFERER']
        updateWorkorderStatus(id,type,pj_id,status_value,request.session['member_id'],url)
        deploy(id,type,pj_id,status_value,request.session['member_id'],url)
        return HttpResponseRedirect('/wk/home/')

    if(type == '1' or type == '2'):
        ret, sl = getWorkorderInfo(id)
        return render(request, 'Workorder/review_order.html',
                      {'order': ret, 'status_list': sl, 'grp_id': request.session['member_grp']})
    elif(type == '3'):
        ret, sl = getWorkorderInfo(id)
        return render(request, 'Workorder/review_db.html',
                      {'order': ret, 'status_list': sl, 'grp_id': request.session['member_grp']})
    elif(type=='5'):
        ret,sl = getWorkorderProjectInfo(id)
        return render(request, 'Workorder/review_project.html',{'order':ret,'status_list': sl,'grp_id': request.session['member_grp']})

def download(request):
    o_id = request.GET['id']
    o_name = request.GET['name']
    file_url = getSqlFileById(o_id)
    def file_iterator(file_url, chunk_size=65535):
        f = open(file_url,"rb")
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
        f.close()
    file_name = o_name + ".sql"
    response = StreamingHttpResponse(file_iterator(file_url))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response
