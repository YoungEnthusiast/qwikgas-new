from django.contrib import admin
from .models import *
from django import forms

class AntiOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created']
    # search_fields = ['name', 'email' 'phone_number', 'date_submitted', 'status']
    # list_filter = ['status']
    # list_display_links = ['email']
    # list_per_page = 10

admin.site.register(AntiOrder, AntiOrderAdmin)
