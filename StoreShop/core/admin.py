from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *


@admin.register(Staffs)
class StaffsAdmin(admin.ModelAdmin):
    fields = ["staff", "is_manager", "is_booker", "is_merchandiser"]
    list_display = ["staff", "is_manager", "is_booker", "is_merchandiser"]

@receiver(post_save, sender=User)
def staff_change(instance, sender, *args, **kwargs):
    if instance.is_staff:
        staff = Staffs.objects.filter(staff=instance)
        if not staff.exists():
            Staffs.objects.create(staff=instance)
    else:
        staff = Staffs.objects.filter(staff=instance).delete()

@admin.register(Categories)
class Categories(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]


@admin.register(Goods)
class Goods(admin.ModelAdmin):
    fields = ["category", "title", "image", "description", "price", "qty"]
    list_display = ["title", "price", "qty"]