# coding=utf-8

from django.db import models


class CartInfo(models.Model):
    '''
        购物车信息
    '''
    user = models.ForeignKey('df_user.UserInfo')
    goods = models.ForeignKey('df_goods.GoodsInfo')
    number = models.IntegerField()