#coding=utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from models import UserInfo,RecvInfo
from login_decorator import verify_login
import hashlib
import sys
from django.core.paginator import Paginator

sys.path.append("..")
from df_goods.models import GoodsInfo
from df_order.models import OrderInfo, OrderDetail


def register(request):

    return render(request, 'df_user/register.html')


def register_handle(request):
    uname = request.POST['user_name']
    upwd = request.POST['pwd']
    cpwd = request.POST['cpwd']
    uemail = request.POST['email']
    if upwd != cpwd:
        pass

    upwd1 = hashlib.sha1()
    upwd1.update(upwd)
    encry_upwd = upwd1.hexdigest()

    user = UserInfo()
    user.uname = uname
    user.upwd = encry_upwd
    user.uemail = uemail
    user.save()
    # print request.POST['email']
    return render(request, 'df_user/register_success.html')


def login(request):
    """"""
    request_path = request.session.get('request_path', '/')
    context = {
        'request_path': request_path,
    }

    return render(request, 'df_user/login.html', context)


def login_handle(request):
    post = request.POST
    uname = post['username']
    upwd = post['password']
    rem_status = post.get('rem_status')
    response_code = {}
    check_uname = UserInfo.objects.filter(uname=uname).count()

    if check_uname == 0:
        response_code['user_exist'] = 0
        response_code['pwd_check'] = 0
        response = JsonResponse({'response_code': response_code})
    else:
        response_code['user_exist'] = 1
        real_password = UserInfo.objects.get(uname=uname).upwd
        m = hashlib.sha1()
        m.update(upwd)
        input_password = m.hexdigest()
        if input_password == real_password:
            response_code['pwd_check'] = 1
            request.session['user_name'] = uname
            request.session['user_id'] = UserInfo.objects.get(uname=uname).pk
            request.session.set_expiry(1800)
        else:
            response_code['pwd_check'] = 0
            pass
        response = JsonResponse({'response_code': response_code})
    # 设置cookie
    if rem_status == "true":
        response.set_cookie('uname', uname)
    else:
        response.delete_cookie('uname')

    return response


def logout(request):
    """"""
    request.session.flush()

    return redirect('/')


def check_exist(request):
    """"""
    check_item = request.GET['item']

    if check_item == 'name':
        check_uname = request.GET['uname']
        count = UserInfo.objects.filter(uname=check_uname).count()
    elif check_item == 'email':
        check_uemail = request.GET['uemail'].replace('%40', '@')
        count = UserInfo.objects.filter(uemail=check_uemail).count()

    return JsonResponse({'count': count})


@verify_login
def userCenter_info(request):

    # uemail = UserInfo.objects.get(pk=request.session.get('user_id')).uemail
    uphone = UserInfo.objects.get(pk=request.session.get('user_id')).uphone
    uaddress = UserInfo.objects.get(pk=request.session.get('user_id')).uaddress
    goods_recentview = request.COOKIES.get('goods_recentview', '')
    try:
        goods_recentview_list = [ int(x) for x in goods_recentview.split(',')]
    except:
        goods_recentview_list = []

    goods_recentview_ob = []

    print goods_recentview_list

    if len(goods_recentview_list) != 0:
        for item in goods_recentview_list:
            goods_recentview_ob.append(GoodsInfo.objects.get(pk=item))

    context = {
        'title': '天天生鲜-用户中心',
        'user_address': uaddress,
        'user_phone': uphone,
        'user_name': request.session.get('user_name', ''),
        'request': request,
        'goods_recentview_ob': goods_recentview_ob,
    }

    return render(request, 'df_user/user_center_info.html', context)


@verify_login
def userCenter_order(request):

    # uemail = UserInfo.objects.get(pk=request.session.get('user_id')).uemail
    # uphone = UserInfo.objects.get(pk=request.session.get('user_id')).uphone
    # uaddress = UserInfo.objects.get(pk=request.session.get('user_id')).uaddress

    page_index = int(request.GET.get('index', 1))
    user_id = int(request.session['user_id'])
    order = OrderInfo.objects.filter(user_id=user_id)[::-1]

    p = Paginator(order, 2)
    page_list = p.page(page_index)

    context = {
        'request': request,
        'order': order,
        'page_list': page_list,
        'page_index': page_index,
    }

    return render(request, 'df_user/user_center_order.html', context)


@verify_login
def userCenter_site(request):

    user_id = request.session.get('user_id')
    user = UserInfo.objects.get(pk=user_id)
    recv1 = user.recvinfo_set.all()
    if len(recv1) == 0:
        recv_username = ''
        recv_addr = ''
        recv_phone = ''
        recv_postcode = ''

    else:
        recv = recv1[0]
        recv_username = recv.recv_username
        recv_addr = recv.recv_addr
        recv_phone = recv.recv_phone
        recv_postcode = recv.recv_postcode

    context = {
        'title': '天天生鲜-用户中心',
        'recv_username': recv_username,
        'recv_addr': recv_addr,
        'recv_phone': recv_phone,
        'recv_postcode': recv_postcode,
        'request': request,
    }

    return render(request, 'df_user/user_center_site.html', context)


def site_handle(request):
    """"""
    user_id = request.session.get('user_id')
    user = UserInfo.objects.get(pk=user_id)
    recv = user.recvinfo_set.all()[0]

    post = request.POST

    recv_username = post.get("recv_username")
    recv_addr = post.get("recv_addr")
    recv_phone = post.get("recv_phone")
    recv_postcode = post.get("recv_postcode")

    recv.recv_username = recv_username
    recv.recv_addr = recv_addr
    recv.recv_phone = recv_phone
    recv.cv_postcode = recv_postcode
    recv.save()
    # print recv.recv_username

    return JsonResponse({'status': 'ok'})
