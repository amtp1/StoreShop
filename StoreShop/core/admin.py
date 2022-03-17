from django.contrib import admin

from .models import *

@admin.register(Staffs)
class Staffs(admin.ModelAdmin):
    fields = ["last_name", "first_name", "position", "birthday", "address", "phone", "note"]
    list_display = ["last_name", "first_name", "position"]


@admin.register(Categories)
class Categories(admin.ModelAdmin):
    fields = ["name", "slug"]
    list_display = ["name", "slug"]


@admin.register(Goods)
class Goods(admin.ModelAdmin):
    fields = ["category", "title", "slug", "image", "description", "price"]
    list_display = ["title", "price"]