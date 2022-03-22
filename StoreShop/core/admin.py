from django.contrib import admin

from .models import *

@admin.register(Staffs)
class Staffs(admin.ModelAdmin):
    fields = ["last_name", "first_name", "position", "birthday", "address", "phone", "note"]
    list_display = ["last_name", "first_name", "position"]


@admin.register(Categories)
class Categories(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]


@admin.register(Goods)
class Goods(admin.ModelAdmin):
    fields = ["category", "title", "image", "description", "price", "qty"]
    list_display = ["title", "price", "qty"]