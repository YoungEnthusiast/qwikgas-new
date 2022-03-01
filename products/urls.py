from django.urls import path
from products import views
from django.contrib.sitemaps.views import sitemap
from products.sitemaps import ProductSitemap

sitemaps={
    'products':ProductSitemap,
}

urlpatterns = [
    path('products', views.product_list, name='product_list'),
    path('sitemap.xml', sitemap, {'sitemaps':sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('<category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<id>/', views.product_detail, name='product_detail'),

    path('product/description/<id>/', views.product_detail2, name='product_detail2'),

    path('qwikvendor-dashboard/products/', views.showQwikVendorProducts, name='qwikvendor_products'),
    path('qwikpartner-dashboard/products/', views.showQwikPartnerProducts, name='qwikpartner_products'),
    path('qwikpartner-dashboard/cylinders-received-empty/', views.showQwikPartnerCylindersReceivedEmpty, name='qwikpartner_cylinders_received_empty'),
    path('qwikvendor-dashboard/cylinders-dispatched-to-plant/', views.showQwikVendorCylindersDispatchedToPlant, name='qwikvendor_cylinders_dispatched_to_plant'),
    path('qwikvendor-dashboard/cylinders-released-filled-to-qwikpartner/', views.showQwikVendorCylindersReleasedFilledToQwikPartner, name='qwikvendor_cylinders_released_filled_to_qwikpartner'),
    path('qwikpartner-dashboard/cylinders-dispatched-filled-to-qwikcustomer/', views.showQwikPartnerCylindersDispatchedFilledToQwikCustomer, name='qwikpartner_cylinders_dispatched_filled_to_qwikcustomer'),
    path('qwika-dashboard/cylinders-dispatched-filled-to-qwikcustomer/', views.showQwikAdminCylindersDispatchedFilledToQwikCustomer, name='qwikadmin_cylinders_dispatched_filled_to_qwikcustomer'),
    path('qwikpartner-dashboard/cylinders-dispatched-filled-to-qwikcustomer/accept/<int:id>', views.acceptQwikPartnerCylindersDispatchedFilledToQwikCustomer, name='accept_qwikpartner_cylinders_dispatched_filled_to_qwikcustomer'),
    path('qwikpartner-dashboard/cylinders-dispatched-filled-to-qwikcustomer/decline/<int:id>', views.declineQwikPartnerCylindersDispatchedFilledToQwikCustomer, name='decline_qwikpartner_cylinders_dispatched_filled_to_qwikcustomer'),
    path('qwika-dashboard/cylinders-dispatched-filled-to-qwikcustomer/accept/<int:id>', views.acceptQwikAdminCylindersDispatchedFilledToQwikCustomer, name='accept_qwikadmin_cylinders_dispatched_filled_to_qwikcustomer'),
    path('qwika-dashboard/cylinders-dispatched-filled-to-qwikcustomer/decline/<int:id>', views.declineQwikAdminCylindersDispatchedFilledToQwikCustomer, name='decline_qwikadmin_cylinders_dispatched_filled_to_qwikcustomer'),
    path('qwikpartner-dashboard/cylinders-dispatched-to-plant/', views.showQwikPartnerCylindersDispatchedToPlant, name='qwikpartner_cylinders_dispatched_to_plant'),
    path('qwikpartner-dashboard/cylinders-delivered-filled-to-qwiklet/', views.showQwikPartnerCylindersDeliveredFilledToQwikLet, name='qwikpartner_cylinders_delivered_filled_to_qwiklet'),
    path('qwikvendor-dashboard/cylinders-delivered-filled-to-qwiklet/', views.showQwikVendorCylindersDeliveredFilledToQwikLet, name='qwikvendor_cylinders_delivered_filled_to_qwiklet'),
    path('qwika-dashboard/cylinders-delivered-filled-to-qwiklet/', views.showQwikAdminCylindersDeliveredFilledToQwikLet, name='qwikadmin_cylinders_delivered_filled_to_qwiklet'),
    path('qwika-dashboard/cylinders-delivered-filled-to-qwiklet/accept/<int:id>', views.acceptQwikAdminCylindersDeliveredFilledToQwikLet, name='accept_qwikadmin_cylinders_delivered_filled_to_qwiklet'),
    path('qwika-dashboard/cylinders-delivered-filled-to-qwiklet/decline/<int:id>', views.declineQwikAdminCylindersDeliveredFilledToQwikLet, name='decline_qwikadmin_cylinders_delivered_filled_to_qwiklet'),
    path('qwikvendor-dashboard/cylinders-delivered-filled-to-qwiklet/accept/<int:id>', views.acceptQwikVendorCylindersDeliveredFilledToQwikLet, name='accept_qwikvendor_cylinders_delivered_filled_to_qwiklet'),
    path('qwikvendor-dashboard/cylinders-delivered-filled-to-qwiklet/decline/<int:id>', views.declineQwikVendorCylindersDeliveredFilledToQwikLet, name='decline_qwikvendor_cylinders_delivered_filled_to_qwiklet'),
    path('qwikpartner-dashboard/cylinders-dispatched-to-plant/accept/<int:id>', views.acceptQwikPartnerCylindersDispatchedToPlant, name='accept_qwikpartner_cylinders_dispatched_to_plant'),
    path('qwikpartner-dashboard/cylinders-dispatched-to-plant/decline/<int:id>', views.declineQwikPartnerCylindersDispatchedToPlant, name='decline_qwikpartner_cylinders_dispatched_to_plant'),
    path('qwika-dashboard/cylinders-dispatched-to-plant/', views.showQwikAdminCylindersDispatchedToPlant, name='qwikadmin_cylinders_dispatched_to_plant'),
    path('qwika-dashboard/cylinders-dispatched-to-plant/accept/<int:id>', views.acceptQwikAdminCylindersDispatchedToPlant, name='accept_qwikadmin_cylinders_dispatched_to_plant'),
    path('qwika-dashboard/cylinders-dispatched-to-plant/decline/<int:id>', views.declineQwikAdminCylindersDispatchedToPlant, name='decline_qwikadmin_cylinders_dispatched_to_plant'),
    path('qwikpartner-dashboard/cylinders-delivered-to-qwikcustomer-anticipatory/', views.showQwikPartnerCylindersDeliveredToQwikCustomerAnti, name='qwikpartner_cylinders_delivered_to_qwikcustomer_anti'),
    path('qwikvendor-dashboard/cylinders-delivered-to-qwikcustomer-anticipatory/', views.showQwikVendorCylindersDeliveredToQwikCustomerAnti, name='qwikvendor_cylinders_delivered_to_qwikcustomer_anti'),
    path('qwika-dashboard/cylinders-delivered-to-qwikcustomer-anticipatory/', views.showQwikAdminCylindersDeliveredToQwikCustomerAnti, name='qwikadmin_cylinders_delivered_to_qwikcustomer_anti'),

    path('qwikcustomer-dashboard/cylinders-received-filled-anticipatory/', views.showQwikCustomerCylindersReceivedFilledAnti, name='qwikcustomer_cylinders_received_filled_anti'),

    path('qwikpartner-dashboard/cylinders-returned-empty/', views.showQwikPartnerCylindersReturnedEmpty, name='qwikpartner_cylinders_returned_empty'),
    path('qwikvendor-dashboard/cylinders-returned-empty/', views.showQwikVendorCylindersReturnedEmpty, name='qwikvendor_cylinders_returned_empty'),
    path('qwikvendor-dashboard/cylinders-returned-empty/accept/<int:id>', views.acceptQwikVendorCylindersReturnedEmpty, name='accept_qwikvendor_cylinders_returned_empty'),
    path('qwikvendor-dashboard/cylinders-returned-empty/decline/<int:id>', views.declineQwikVendorCylindersReturnedEmpty, name='decline_qwikvendor_cylinders_returned_empty'),
    path('qwika-dashboard/cylinders-returned-empty/accept/<int:id>', views.acceptQwikAdminCylindersReturnedEmpty, name='accept_qwikadmin_cylinders_returned_empty'),
    path('qwika-dashboard/cylinders-returned-empty/decline/<int:id>', views.declineQwikAdminCylindersReturnedEmpty, name='decline_qwikadmin_cylinders_returned_empty'),
    path('qwika-dashboard/cylinders-received-empty/', views.showQwikAdminCylindersReceivedEmpty, name='qwikadmin_cylinders_received_empty'),
    path('qwika-dashboard/cylinders-returned-empty/', views.showQwikAdminCylindersReturnedEmpty, name='qwikadmin_cylinders_returned_empty'),
    path('qwika-dashboard/cylinders-received-empty/update/<int:id>', views.updateQwikAdminCylindersReceivedEmpty, name='update_qwikadmin_cylinders_received_empty'),
    path('qwika-dashboard/cylinders-returned-empty/update/<int:id>', views.updateQwikAdminCylindersReturnedEmpty, name='update_qwikadmin_cylinders_returned_empty'),
    path('qwika-dashboard/cylinders-dispatched-to-plant/update/<int:id>', views.updateQwikAdminCylindersDispatchedToPlant, name='update_qwikadmin_cylinders_dispatched_to_plant'),
    path('qwika-dashboard/cylinders-dispatched-filled-to-qwikcustomer/update/<int:id>', views.updateQwikAdminCylindersDispatchedFilledToQwikCustomer, name='update_qwikadmin_cylinders_dispatched_filled_to_qwikcustomer'),
    path('qwikcustomer-dashboard/cylinders-returned-empty/', views.showQwikCustomerCylindersReturnedEmpty, name='qwikcustomer_cylinders_returned_empty'),
    path('qwika-dashboard/products/', views.showQwikAdminProducts, name='qwikadmin_products'),
    path('qwikvendor-dashboard/products/update/<int:id>', views.updateQwikVendorProducts, name='update_products'),
    path('qwika-dashboard/products/update/<int:id>', views.updateProduct, name='qwikadmin_update_products'),
    path('qwika-dashboard/product/add-new', views.addProduct, name='qwikadmin_product'),
    path('qwika-dashboard/products/delete/<int:id>', views.deleteProduct),
    path('qwikpartner-dashboard/products/update/<int:id>', views.updateQwikPartnerProducts, name='update_products_partner'),
    # path('<id>/<slug>/', views.product_detail, name='product_detail'),
    # path('fund-wallet', views.fundWallet, name='fund'),
]
