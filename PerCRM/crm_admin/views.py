# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from crm_admin import enabled_admins
from models import  *

# Create your views here.
def index(request):
    context = {
        'username': request.user,
        'enabled_admins': enabled_admins,
    }
    return render(request, 'crm_admin/index.html', context)


def handle_tables(request, models, table):
    '''
    models = crm, table = customer,
    enabled_admins = {
        'crm': {
              'customer': <class 'crm_admin.crm_admin.CustomerAdmin'>,
              'tags': <class 'crm_admin.crm_admin.TagsAdmin'>}
         }
    }

    '''

    page_index = request.GET.get('page', 1)

    parent_url = models
    current_url = table

    table_admin_obj = enabled_admins[models][table]
    page_numbers = table_admin_obj.list_per_page
    table_obj = table_admin_obj.models.objects.order_by('-id')

    table_obj_display_list = table_admin_obj.list_display
    table_obj_head_dict = table_admin_obj.get_head_name()
    table_obj_head_list = []

    for item in table_obj_display_list:
        table_obj_head_list.append(table_obj_head_dict[item].upper())

    p = Paginator(table_obj, page_numbers)
    page_list = p.page(page_index)


    context = {
        'username': request.user,
        'tableObj': table_obj,
        'tableObjDisplayList': table_obj_display_list,
        'tableObjHeadList': table_obj_head_list,
        'parent_url': parent_url,
        'current_url': current_url,
        'page_list': page_list,
        'page_index': page_index,
    }

    return render(request, 'crm_admin/table_index.html', context)


def handle_models(request, table):
    context = {
        'username': request.user,
        'enabled_admins': enabled_admins,
    }

    return render(request, 'crm_admin/models_index.html', context)


def change_tables(request, models, table, table_ins):

    model = enabled_admins[models][table].models.objects.get(id=int(table_ins))
    model_fields = [ type(x).__name__ for x in model._meta.fields ]

    parent1_url = models
    parent2_url = table

    context = {
        'username': request.user,
        'enabled_admins': enabled_admins,
        'parent1_url': parent1_url,
        'parent2_url': parent2_url,
        'model': model,
        'model_fields': model_fields,
    }

    return render(request, 'crm_admin/table_change.html', context)