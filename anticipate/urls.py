from django.urls import path
from . import views

urlpatterns = [
    path('anticipatory-orders', views.showAntiOrders, name='anti_orders'),

    # path('orders/checkout/<str:pk>/', views.showOrder, name='show_order'),
    # path('orders/invoice/<str:pk>/', views.showInvoice, name='show_invoice'),
    # path('qwikvendor-dashboard/orders/invoice/<str:pk>/', views.showQwikVendorInvoice, name='show_vendor_invoice'),
    # path('qwikpartner-dashboard/orders/invoice/<str:pk>/', views.showQwikPartnerInvoice, name='show_partner_invoice'),
    # path('qwika-dashboard/orders/invoice/<str:pk>/', views.showQwikAdminInvoice, name='show_admin_invoice'),
    # path('card-payment', views.showPaymentComplete, name='payment_complete'),
    # path('orders/checkout/<str:pk>/pay', views.updateWallet),
    # path('qwikcustomer-dashboard/orders/', views.showOrderItems, name='order_items'),
    # path('qwika-dashboard/orders/', views.showQwikAdminOrders, name='qwikadmin_orders'),
    # path('qwikvendor-dashboard/orders/', views.showQwikVendorOrders, name='qwikvendor_orders'),
    # path('qwikvendor-dashboard/order-items/', views.showQwikVendorOrderItems, name='qwikvendor_order_items'),
    # path('qwikpartner-dashboard/order-items/', views.showQwikPartnerOrderItems, name='qwikpartner_order_items'),
    # path('qwika-dashboard/order-items/', views.showQwikAdminOrderItems, name='qwikadmin_order_items'),
    # path('qwikvendor-dashboard/order-items/add-status/<int:id>', views.addOrderStatusQwikVendor, name='qwikvendor_order_status'),
    # path('qwikpartner-dashboard/order-items/add-status/<int:id>', views.addOrderStatusQwikPartner, name='qwikpartner_order_status'),
    # path('qwikvendor-dashboard/order-statuses/', views.showQwikVendorOrderStatuses, name='qwikvendor_order_statuses'),
    # path('qwikcustomer-dashboard/order-statuses/', views.showOrderStatuses, name='order_statuses'),
    # path('qwikpartner-dashboard/order-statuses/', views.showQwikPartnerOrderStatuses, name='qwikpartner_order_statuses'),
    #path('qwikpartner-dashboard/anticipatory-order/add-new', views.addQwikPartnerAntiOrder, name='qwikpartner_anti_order'),
    path('qwikvendor-dashboard/anticipatory-orders/', views.showQwikVendorAntiOrders, name='qwikvendor_anti_orders'),
    path('qwikvendor-dashboard/anticipatory-orders/update/<int:id>', views.updateQwikVendorAntiOrders, name='qwikvendor_update_anti_orders'),
    path('qwikpartner-dashboard/anticipatory-orders/', views.showQwikPartnerAntiOrders, name='qwikpartner_anti_orders'),
    path('qwikpartner-dashboard/anticipatory-orders/update/<int:id>', views.updateQwikPartnerAntiOrders, name='qwikpartner_update_anti_order'),
    path('qwikpartner-dashboard/anticipatory-orders/payment-update/<int:id>', views.updateQwikPartnerAntiOrders3rd, name='qwikpartner_update_anti_order_3rd'),
    path('qwikpartner-dashboard/anticipatory-orders/invoice/<str:pk>/', views.showQwikPartnerAntiInvoice, name='show_partner_anti_invoice'),
    path('qwikvendor-dashboard/anticipatory-orders/invoice/<str:pk>/', views.showQwikVendorAntiInvoice, name='show_vendor_anti_invoice'),
    path('qwikcustomer-dashboard/anticipatory-orders/invoice/<str:pk>/', views.showAntiInvoice, name='show_anti_invoice'),

    # # path('visitor-order', views.order_visitor, name='order_visitor'),
    # # path('st---only2', views.addOrder, name='add_order'),
    # path('qwikcustomer-address/order/<int:id>', views.showAddressCust, name='qwikcust_address'),
]
