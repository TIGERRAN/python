# coding=utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from models import OrderInfo, OrderDetail

from datetime import datetime
from decimal import Decimal
import sys
sys.path.append('..')
from df_user.login_decorator import verify_login
from df_user.models import UserInfo, RecvInfo
from df_goods.models import GoodsInfo
from df_cart.models import CartInfo


@verify_login
def index(request):
    '''
        订单首页显示
    '''
    user_id = int(request.session['user_id'])
    goods_id_lists = request.GET.getlist('goods_id')

    user = UserInfo.objects.get(id=user_id)
    recvinfo = user.recvinfo_set.all()[0]

    goods_list = []
    for item in goods_id_lists:
        goods = GoodsInfo.objects.get(id=int(item))
        goods1 = CartInfo.objects.get(goods_id=item, user_id=user_id)
        goods_number = goods1.number

        a = {
            'obj': goods,
            'number': goods_number,

        }

        goods_list.append(a)

    context = {
        'goodsinfo': goods_list,
        'user': user,
        'recvinfo': recvinfo,
    }

    return render(request, 'df_order/place_order.html', context)


@transaction.atomic()
@verify_login
def handle_order(request):
    '''
        处理订单
    '''
    # 定义事务id
    tran_id = transaction.savepoint()

    goods_ids1 = request.POST.get('goods_ids')
    total = request.POST.get('total')
    goods_ids = goods_ids1.split(',')[:-1]
    address = request.POST.get('address')

    try:
        # 创建订单对象
        order = OrderInfo()
        # 定义创建订单时间对象
        now = datetime.now()
        # 获取uid
        user_id = int(request.session['user_id'])

        # 赋值订单各信息
        order.oid = '{}{}'.format(now.strftime('%Y%m%d%H%M%S'), user_id)
        order.user_id = user_id
        order.odate = now
        order.oTotal = Decimal(total)
        order.oaddress = address
        order.save()

        # 存入订单详情信息
        for item in goods_ids:
            detail = OrderDetail()
            detail.order = order
            cart = CartInfo.objects.get(goods_id=item, user_id=user_id)
            detail.goods_id = item
            goods = GoodsInfo.objects.get(id=item)
            detail.price = goods.gprice
            detail.count = cart.number
            detail.save()

        transaction.savepoint_commit(tran_id)

    except Exception as e:
        print '==============', e
        transaction.savepoint_rollback(tran_id)

    return JsonResponse({'status': 'ok'})