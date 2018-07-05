# coding=utf-8

from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from models import TypeInfo, GoodsInfo


def verify_nologin(func):
    def wrapper(request, *args):
        if request.session.get('user_name', 0) == 0:
            request.session['request_path'] = request.get_full_path()
        if len(args) == 0:
            return func(request)
        else:
            return func(request, args[0])

    return wrapper


def index(request):
    context = {}
    typeinfo_list = TypeInfo.objects.all()
    for item in typeinfo_list:
        typename = 'type' + str(item.id)
        typename_newlist = typename + 'n'
        typename_hotlist = typename + 'h'
        newlist = item.goodsinfo_set.all().order_by('-id')[:4]
        hotlist = item.goodsinfo_set.all().order_by('-gclick')[:4]
        context[typename_newlist] = newlist
        context[typename_hotlist] = hotlist
        context['request'] = request

    # return render(request, 'df_goods/index_back.html', context)
    return render(request, 'df_goods/index.html', context)


@verify_nologin
def list(request):
    type_id = request.GET['tid']
    page_index = request.GET['index']
    sort = request.GET['sort']

    context = {}

    type_object = TypeInfo.objects.get(pk=int(type_id))
    new_list = type_object.goodsinfo_set.all().order_by('-id')[:2]
    context['new_list'] = new_list

    if sort == "0":
        goods_lists = type_object.goodsinfo_set.all().order_by('-id')
    elif sort == "1":
        goods_lists = type_object.goodsinfo_set.all().order_by('-gprice')
    elif sort == "2":
        goods_lists = type_object.goodsinfo_set.all().order_by('-gclick')

    p = Paginator(goods_lists, 10)
    page_list = p.page(page_index)

    context =  {
        'type_id': type_id,
        'sort': sort,
        'page_index': page_index,
        'type_object': type_object,
        'new_list': new_list,
        'goods_lists': goods_lists,
        'page_list': page_list,
        'request': request,
    }

    return render(request, 'df_goods/list.html', context)


@verify_nologin
def detail(request, id):
    """"""
    goods_info = GoodsInfo.objects.get(pk=int(id))
    goods_info.gclick += 1
    goods_info.save()

    new_list = goods_info.gtype.goodsinfo_set.all().order_by('-id')[:2]

    context = {
        'goods_info': goods_info,
        'new_list': new_list,
        'request': request,
    }

    response = render(request, 'df_goods/detail.html', context)

    goods_recentview = request.COOKIES.get('goods_recentview', '')

    if goods_recentview != '':
        goods_recentview1 = goods_recentview.split(',')
        if goods_recentview1.count(str(goods_info.id))>=1:
            goods_recentview1.remove(str(goods_info.id))
        goods_recentview1.insert(0, str(goods_info.id))

        if len(goods_recentview1)>=6:
            del goods_recentview1[5]
        goods_recentview = ','.join(goods_recentview1)
    else:
        goods_recentview = str(goods_info.id)

    response.set_cookie('goods_recentview', goods_recentview)

    return response



