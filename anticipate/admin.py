from django.contrib import admin
from .models import *
from django import forms

class AntiOrderAdmin(admin.ModelAdmin):
    list_display = ['created', 'user', 'static_price2']
    # search_fields = ['name', 'email' 'phone_number', 'date_submitted', 'status']
    # list_filter = ['status']
    # list_display_links = ['email']
    # list_per_page = 10
    list_editable = ['static_price2']

admin.site.register(AntiOrder, AntiOrderAdmin)
