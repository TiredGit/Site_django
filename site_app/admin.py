from django.contrib import admin
from site_app import models


@admin.register(models.MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')


@admin.register(models.Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'grade')