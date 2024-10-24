from django.contrib import admin
from site_app import models

@admin.register(models.MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'birthday')