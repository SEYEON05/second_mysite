from django.contrib import admin
from .models import *


@admin.register(Menu_Cate)
class MenuCateAdmin(admin.ModelAdmin):
  list_display = ['id', 'cate_name']

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
  list_display = ['menu_name', 'price', 'cate']
  extra = 5

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ['nickname', 'ordered_menu', 'ordered_date']



