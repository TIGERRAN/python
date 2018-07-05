# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from crm.models import *
from django import template
import importlib


register = template.Library()


@register.simple_tag
def rend_admin_class(admin_class):
    return admin_class.models._meta.verbose_name_plural


@register.simple_tag
def getVerboseName(model):
    return model._meta.verbose_name_plural


@register.simple_tag
def reduce_attr(attr1, attr2):
    if attr2 == 'date':
        res = getattr(attr1, attr2).strftime("%Y-%m-%d %H:%M:%S")
    else:
        if hasattr(attr1, 'get_{}_display'.format(attr2)):
            res = getattr(attr1, 'get_{}_display'.format(attr2))()
        else:
            res = getattr(attr1, attr2)
    return res


@register.simple_tag
def get_field(model):

    return model._meta.get_fields()


@register.simple_tag
def get_field_info(model, field):

    try:
        field_info = {
            'field_name': getattr(model, field.name),
            'field_type': type(field).__name__,
        }
    except:
        field_info = {}


    return field_info


@register.simple_tag
def get_int_choices(model, field):

    res = {}

    if hasattr(model, 'get_{}_display'.format(field.name)):
        res['status'] = 1
        res['choices'] = field.choices
        res['selected'] = getattr(model, 'get_{}_display'.format(field.name))()
    else:
        res['status'] = 0

    return res


@register.simple_tag
def get_foreignkey_info(model, field):
    relate_model = field.related_model
    relate_model_list = relate_model.objects.all()
    relate_model_self = getattr(model, field.name)

    res = {
        'relate_model_list': relate_model_list,
        'relate_model_self': relate_model_self,
    }

    return res


