from django.contrib import admin
from .models import Category, Product, Cylinder, Owing

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['created', 'updated', 'type', 'mass', 'price', 'image']
    search_fields = ['type', 'price']
    list_editable = ['price']
    prepopulated_fields = {'slug': ('type',)}
admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['created', 'product_Id', 'category', 'partner_product_status', 'vendor_product_status']
    # search_fields = ['type', 'price']
    list_filter = ['category']
    list_display_links = ['product_Id']
    # list_editable = ['price']
    #prepopulated_fields = {'slug': ('type',)}
    list_per_page = 10

admin.site.register(Product, ProductAdmin)

class CylinderAdmin(admin.ModelAdmin):
    list_display = ['created', 'cylinder', 'customer_product_status', 'vendor_product_status', 'partner_product_status', 'admin_product_status']
    # search_fields = ['type', 'price']
    list_display_links = ['cylinder']
    # list_editable = ['price']
    #prepopulated_fields = {'slug': ('type',)}
    list_per_page = 10

admin.site.register(Cylinder, CylinderAdmin)

class OwingAdmin(admin.ModelAdmin):
    list_display = ['created', 'cylinder', 'customer']
    # search_fields = ['type', 'price']
    list_display_links = ['cylinder']
    # list_editable = ['price']
    #prepopulated_fields = {'slug': ('type',)}
    list_per_page = 10

admin.site.register(Owing, OwingAdmin)
