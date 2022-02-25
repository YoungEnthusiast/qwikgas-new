from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['type']
    prepopulated_fields = {'slug': ('type',)}
admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['created', 'updated', 'type', 'category', 'price', 'image']
    search_fields = ['type', 'price']
    list_filter = ['type', 'created', 'updated', 'category']
    list_display_links = ['type', 'image']
    list_editable = ['price']
    prepopulated_fields = {'slug': ('type',)}
    list_per_page = 10

admin.site.register(Product, ProductAdmin)
