# coding=utf-8

from django.db import models


class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=30)
    uphone = models.CharField(max_length=11)
    uaddress = models.CharField(max_length=100)

    def __str__(self):
        return self.uname.encode('utf-8')


class RecvInfo(models.Model):
    """"""
    recv_username = models.CharField(max_length=20)
    recv_addr = models.CharField(max_length=100)
    recv_phone = models.CharField(max_length=11)
    recv_postcode = models.CharField(max_length=6)
    uid = models.ForeignKey('UserInfo')

    def __str__(self):
        return self.recv_username.encode('utf-8')

