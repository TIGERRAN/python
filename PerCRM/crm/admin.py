# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'qq', 'phone', 'source', 'consultant', 'consult_course', 'status', 'date']
    list_per_page = 5
    # 页面可操作
    list_editable = ['status']


class TagsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


# Register your models here.
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(CustomerFollowUp)
admin.site.register(Course)
admin.site.register(ClassList)
admin.site.register(Branch)
admin.site.register(CourseRecord)
admin.site.register(StudyRecord)
admin.site.register(Enrollment)
admin.site.register(Payment)
admin.site.register(Role)
admin.site.register(UserProfile)
admin.site.register(Menu)


