# coding=utf-8

from django.shortcuts import render
from django.http import JsonResponse
from models import CartInfo
import sys
sys.path.append('..')
from df_user.login_decorator import verify_login


def verify_action(func):
    def wrapper(request, *args):
        if request.session.get('user_name', 0) == 0:
            # request.session['request_path'] = request.get_full_path()
            return JsonResponse({'status': 'error'})
        else:
            if len(args) == 0:
                return func(request)
            else:
                # return func(request, args[0])
                pass
    return wrapper



@verify_login
def cart(request):
    user_id = request.session.get('user_id', 0)
    if user_id:
        carts = CartInfo.objects.filter(user_id=user_id)

    context = {
        'carts': carts,
        'request': request,
    }

    return render(request, 'df_cart/cart.html', context)


@verify_action
def getinfo(request):
    '''
       获取购物车相关信息
    '''
    cartinfo = {}
    cartinfo['goods_number'] = {}
    user_id = request.session.get('user_id')
    carts = CartInfo.objects.filter(user_id=user_id)
    for cart in carts:
        cartinfo['goods_number'][str(cart.goods.id)] = cart.number

    cartinfo['number'] = len(carts)
    return JsonResponse(cartinfo)


@verify_action
def add(request):
    '''添加购物车,uid, gid, count,
       如果购物车中存在，加入购物车的操作编程count+, 若不存在，存入gid且count+
    '''
    user_id = int(request.session['user_id'])

    goods_id = int(request.GET['goods_id'])
    goods_count = int(request.GET['goods_count'])

    if CartInfo.objects.filter(user_id=user_id, goods_id=goods_id):
        cart = CartInfo.objects.get(user_id=user_id, goods_id=goods_id)
        cart.number += goods_count
    else:
        cart = CartInfo()
        cart.user_id = user_id
        cart.goods_id = goods_id
        cart.number = goods_count

    cart.save()
    return JsonResponse({'status': 'ok', 'cart_number': len(CartInfo.objects.filter(user_id=user_id))})


@verify_action
def delete(request):
    '''
        删除goods_id,
    '''
    user_id = int(request.session['user_id'])
    goods_id = int(request.GET['goods_id'])
    goods = CartInfo.objects.get(goods_id=goods_id, user_id=user_id)
    goods.delete()

    return JsonResponse({'status': 'ok'})


@verify_action
def edit(request):
    '''
        修改cart信息
    '''
    user_id = int(request.session['user_id'])
    goods_id = int(request.GET['goods_id'])
    goods_number = int(request.GET['number'])
    goods = CartInfo.objects.get(goods_id=goods_id, user_id=user_id)
    goods.number = goods_number
    goods.save()

    return JsonResponse({'status': 'ok'})