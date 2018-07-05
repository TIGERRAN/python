# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from crm.models import *


enabled_admins = {}


class BaseAdmin(object):
    list_display = []
    filter_display = []
    list_per_page = None

    @classmethod
    def get_head_name(cls):
        head_name = {}
        for field in cls.models._meta.fields:
            if field.name in cls.list_display:
                head_name[field.name] = field.verbose_name

        return head_name


class CustomerAdmin(BaseAdmin):
    '''
    定义显示字段
    '''
    list_display = ['id' , 'name', 'qq', 'status', 'source','consultant', 'date']
    list_per_page = 5


class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ['id', 'customer', 'content', 'intention', 'date']


class TagsAdmin(BaseAdmin):
    '''
    定义显示字段
    '''
    list_display = ['id', 'name']


class CourseAdmin(BaseAdmin):
    list_display = ['id', 'name', 'price', 'period', 'outline']
    list_per_page = 5

def register(models, admin_models=None):
    if models._meta.app_label not in enabled_admins:
        enabled_admins[models._meta.app_label] = {}
    # 关联类
    admin_models.models = models
    # 获取字典信息， 例如 enabled_admins['crm']['customer'] = CustomerAdmin
    enabled_admins[models._meta.app_label][models._meta.model_name] = admin_models


register(Customer, CustomerAdmin)
register(Tags, TagsAdmin)
register(CustomerFollowUp, CustomerFollowUpAdmin)
register(Course, CourseAdmin)