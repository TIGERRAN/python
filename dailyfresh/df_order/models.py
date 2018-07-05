# coding=utf-8

from django.db import models
from datetime import datetime
# from pytz import utc

class OrderInfo(models.Model):
    '''
        订单信息
    '''
    oid = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey('df_user.UserInfo')
    odate = models.DateTimeField(auto_now=True) # , default=datetime.now().replace(tzinfo=utc)
    oIsPay = models.BooleanField(default=False)
    oTotal = models.DecimalField(max_digits=6, decimal_places=2)
    oaddress = models.CharField(max_length=120)


class OrderDetail(models.Model):
    '''
        订单详情信息
    '''
    goods = models.ForeignKey('df_goods.GoodsInfo')
    order = models.ForeignKey('OrderInfo')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    count = models.IntegerField()



