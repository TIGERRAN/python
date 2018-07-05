from django.contrib import admin
from models import GoodsInfo,TypeInfo


class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttitle', 'isDelete']


class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'gtitle', 'gprice', 'gunit', 'gclick', 'gintroduction', 'gstock', 'gcontent', 'gtype']


admin.site.register(TypeInfo, TypeInfoAdmin)
admin.site.register(GoodsInfo, GoodsInfoAdmin)
