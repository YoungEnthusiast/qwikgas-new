from django.urls import path
from . import views

urlpatterns = [
    path('order', views.createOrder, name='order_create'),
    path('orders', views.showOrders, name='orders'),
    path('orders/delete/<int:id>', views.deleteOrder),
    path('orders/checkout/<str:pk>/', views.showOrder, name='show_order'),
    path('orders/checkout/pay-later', views.addPayLater, name='qwikcustomer_pay_later'),
    path('orders/checkout/pay-small-small', views.addPaySmall, name='qwikcustomer_pay_small'),

    path('orders/invoice/<str:pk>/', views.showInvoice, name='show_invoice'),
    path('orders/invoice//unpaid/<str:pk>/', views.showInvoiceUnPaid, name='show_invoice_unpaid'),
    path('qwikvendor-dashboard/orders/invoice/<str:pk>/', views.showQwikVendorInvoice, name='show_vendor_invoice'),
    path('qwikpartner-dashboard/orders/invoice/<str:pk>/', views.showQwikPartnerInvoice, name='show_partner_invoice'),
    path('qwika-dashboard/orders/invoice/<str:pk>/', views.showQwikAdminInvoice, name='show_admin_invoice'),
    path('card-payment', views.showPaymentComplete, name='payment_complete'),
    path('orders/checkout/<str:pk>/pay', views.updateWallet),
    path('qwikcustomer-dashboard/orders/', views.showOrderItems, name='order_items'),
    path('qwika-dashboard/orders/', views.showQwikAdminOrders, name='qwikadmin_orders'),
    path('qwikvendor-dashboard/orders/', views.showQwikVendorOrders, name='qwikvendor_orders'),
    path('qwikvendor-dashboard/order-items/', views.showQwikVendorOrderItems, name='qwikvendor_order_items'),
    path('qwikpartner-dashboard/order-items/', views.showQwikPartnerOrderItems, name='qwikpartner_order_items'),
    path('qwika-dashboard/order-items/', views.showQwikAdminOrderItems, name='qwikadmin_order_items'),
    path('qwikvendor-dashboard/order-items/add-status/<int:id>', views.addOrderStatusQwikVendor, name='qwikvendor_order_status'),
    path('qwikpartner-dashboard/order-items/add-status/<int:id>', views.addOrderStatusQwikPartner, name='qwikpartner_order_status'),
    path('qwikvendor-dashboard/order-statuses/', views.showQwikVendorOrderStatuses, name='qwikvendor_order_statuses'),
    path('qwikcustomer-dashboard/order-statuses/', views.showOrderStatuses, name='order_statuses'),
    path('qwikpartner-dashboard/order-statuses/', views.showQwikPartnerOrderStatuses, name='qwikpartner_order_statuses'),
    path('qwikpartner-dashboard/orders/', views.showQwikPartnerOrders, name='qwikpartner_orders'),
    # path('visitor-order', views.order_visitor, name='order_visitor'),
    # path('st---only2', views.addOrder, name='add_order'),
    path('qwikcustomer-address/order/<int:id>', views.showAddressCust, name='qwikcust_address'),
]
