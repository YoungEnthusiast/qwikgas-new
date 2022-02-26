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
    path('qwikpartner-dashboard/cylinders-returned-empty/', views.showQwikPartnerCylindersReturnedEmpty, name='qwikpartner_cylinders_returned_empty'),
    path('qwikvendor-dashboard/cylinders-returned-empty/', views.showQwikVendorCylindersReturnedEmpty, name='qwikvendor_cylinders_returned_empty'),
    path('qwikvendor-dashboard/cylinders-returned-empty/Accept/<int:id>', views.acceptQwikVendorCylindersReturnedEmpty, name='accept_qwikvendor_cylinders_returned_empty'),

    path('qwika-dashboard/cylinders-received-empty/', views.showQwikAdminCylindersReceivedEmpty, name='qwikadmin_cylinders_received_empty'),
    path('qwika-dashboard/cylinders-returned-empty/', views.showQwikAdminCylindersReturnedEmpty, name='qwikadmin_cylinders_returned_empty'),
    path('qwika-dashboard/cylinders-received-empty/update/<int:id>', views.updateQwikAdminCylindersReceivedEmpty, name='update_qwikadmin_cylinders_received_empty'),

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
