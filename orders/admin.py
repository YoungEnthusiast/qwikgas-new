from django.contrib import admin
from .models import UserOrder, OrderItem, OrderStatus, PayDelivery, PayLater, PaySmall
#from django.contrib.gis import admin

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product', 'price', 'quantity', 'get_cost']
    fields = ['product', 'price', 'quantity', 'get_cost']
    raw_id_fields = ['product']

class UserOrderAdmin(admin.ModelAdmin):
    list_display = ['created', 'order_Id', 'user', 'address', 'get_total_cost', 'payment_status']
    search_fields = ['order_Id', 'user__username', 'user__email', 'payment_Mode', 'created', 'updated']
    list_filter = ['payment_status']
    list_display_links = ['order_Id', 'user']
    list_per_page = 10
    inlines = [OrderItemInline]

admin.site.register(UserOrder, UserOrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'price', 'quantity']
    # search_fields = ['order_Id', 'user__username', 'user__email', 'payment_Mode', 'created', 'updated', 'order_status']
    # list_filter = ['order_status', 'payment_status']
    list_display_links = ['product']
    list_per_page = 10

admin.site.register(OrderItem, OrderItemAdmin)

class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ['created', 'updated', 'order']
    search_fields = ['created', 'updated', 'order__order_Id']
    list_filter = []
    list_display_links = ['order']
    list_per_page = 10

admin.site.register(OrderStatus, OrderStatusAdmin)

class PayDeliveryAdmin(admin.ModelAdmin):
    # list_display = ['created', 'updated', 'order']
    # search_fields = ['created', 'updated', 'order__order_Id']
    # list_filter = []
    # list_display_links = ['order']
    list_per_page = 10

admin.site.register(PayDelivery, PayDeliveryAdmin)

class PayLaterAdmin(admin.ModelAdmin):
    # list_display = ['created', 'updated', 'order']
    # search_fields = ['created', 'updated', 'order__order_Id']
    # list_filter = []
    # list_display_links = ['order']
    list_per_page = 10

admin.site.register(PayLater, PayLaterAdmin)

class PaySmallAdmin(admin.ModelAdmin):
    # list_display = ['created', 'updated', 'order']
    # search_fields = ['created', 'updated', 'order__order_Id']
    # list_filter = []
    # list_display_links = ['order']
    list_per_page = 10

admin.site.register(PaySmall, PaySmallAdmin)
