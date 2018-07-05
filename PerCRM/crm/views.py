# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

# Create your views here.
def index(request):
    context = {
        'username': request.user
    }

    return render(request, 'crm/index_back.html', context)


def sale(request):
    li_id = request.GET.get('id')
    context = {
        'username': request.user,
        'li_id': li_id,
    }

    return render(request, 'crm/sale/index_back.html', context)


def student(request):
    li_id = request.GET.get('id')
    context = {
        'username': request.user,
        'li_id': li_id,
    }

    return render(request, 'crm/student/index_back.html', context)


def teacher(request):
    li_id = request.GET.get('id')
    context = {
        'username': request.user,
        'li_id': li_id,
    }

    return render(request, 'crm/teacher/index_back.html', context)



