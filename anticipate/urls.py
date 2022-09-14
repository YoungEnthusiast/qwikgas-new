from django.urls import path
from . import views

urlpatterns = [
    path('anticipatory-orders', views.showAntiOrders, name='anti_orders'),
    path('qwikvendor-dashboard/anticipatory-orders/', views.showQwikVendorAntiOrders, name='qwikvendor_anti_orders'),
    path('qwikvendor-dashboard/anticipatory-orders/update/<int:id>', views.updateQwikVendorAntiOrders, name='qwikvendor_update_anti_orders'),
    path('qwikpartner-dashboard/anticipatory-orders/', views.showQwikPartnerAntiOrders, name='qwikpartner_anti_orders'),
    path('qwika-dashboard/anticipatory-orders/', views.showQwikAdminAntiOrders, name='qwikadmin_anti_orders'),
    path('qwika-dashboard/sales-graph/', views.showQwikAdminSalesGraph, name='qwikadmin_sales_graph'),
    path('qwika-dashboard/anticipatory-credits/', views.showQwikAdminAntiCredits, name='qwikadmin_anti_credits'),
    path('qwika-dashboard/anticipatory-payments/', views.showQwikAdminAntiPayments, name='qwikadmin_anti_payments'),
    path('qwika-dashboard/anticipatory-sales/', views.showQwikAdminAntiSales, name='qwikadmin_anti_sales'),
    path('qwikpartner-dashboard/anticipatory-orders/update/<int:id>', views.updateQwikPartnerAntiOrders, name='qwikpartner_update_anti_order'),
    path('qwikpartner-dashboard/anticipatory-orders/payment-update/<int:id>', views.updateQwikPartnerAntiOrders3rd, name='qwikpartner_update_anti_order_3rd'),
    path('qwikpartner-dashboard/anticipatory-orders/invoice/<str:pk>/', views.showQwikPartnerAntiInvoice, name='show_partner_anti_invoice'),
    path('qwikvendor-dashboard/anticipatory-orders/invoice/<str:pk>/', views.showQwikVendorAntiInvoice, name='show_vendor_anti_invoice'),
    path('qwikcustomer-dashboard/anticipatory-orders/invoice/<str:pk>/', views.showAntiInvoice, name='show_anti_invoice'),
    path('qwikcustomer-dashboard/anticipatory-orders/invoice/unpaid/<str:pk>/', views.showAntiInvoiceUnPaid, name='show_anti_invoice_unpaid'),
    path('qwika-dashboard/anticipatory-orders/export-csv', views.exportCSVAntis, name='export_csv_anti'),
    path('qwika-dashboard/anticipatory-credits/export-csv', views.exportCSVCredits, name='export_csv_credit'),
    path('qwika-dashboard/anticipatory-payments/export-csv', views.exportCSVPayments, name='export_csv_payment'),
    path('qwika-dashboard/anticipatory-orders/randomized', views.randomize, name='qwikadmin_randomize'),
    # path('qwika-dashboard/anticipatory-orders/export-pdf', views.exportPDF, name='export_pdf'),
]
