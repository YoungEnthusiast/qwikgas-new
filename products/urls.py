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
    path('cylinders/histories/', views.showQwikCustomerCylinders, name='qwikcustomer_cylinders'),
    path('cylinders/histories/update/<int:id>', views.updateQwikCustomerCylinders, name='update_cylinders'),

    path('qwikvendor-dashboard/products/', views.showQwikVendorProducts, name='qwikvendor_products'),
    path('qwikvendor-dashboard/cylinders/', views.showQwikVendorCylinders, name='qwikvendor_cylinders'),
    path('qwikpartner-dashboard/products/', views.showQwikPartnerProducts, name='qwikpartner_products'),
    path('qwikpartner-dashboard/cylinders/', views.showQwikPartnerCylinders, name='qwikpartner_cylinders'),
    path('qwikpartner-dashboard/cylinders-received-empty/', views.showQwikPartnerCylindersReceivedEmpty, name='qwikpartner_cylinders_received_empty'),
    path('qwika-dashboard/products/', views.showQwikAdminProducts, name='qwikadmin_products'),
    path('qwika-dashboard/cylinders-histories/', views.showQwikAdminAdmCylinders, name='qwikadmin_adm_cylinders'),
    path('qwika-dashboard/cylinders/', views.showQwikAdminCylinders, name='qwikadmin_cylinders'),
    path('qwikvendor-dashboard/products/update/<int:id>', views.updateQwikVendorProducts, name='update_products'),
    path('qwikvendor-dashboard/cylinders/update/<int:id>', views.updateQwikVendorCylinders, name='update_cylinders'),
    path('qwikpartner-dashboard/cylinders/update/<int:id>', views.updateQwikPartnerCylinders, name='update_cylinders_partner'),
    path('qwika-dashboard/cylinders-histories/update/<int:id>', views.updateQwikAdminAdmCylinders, name='update_cylinders_admin'),
    path('qwikvendor-dashboard/cylinder/add-new', views.addQwikVendorCylinder, name='qwikvendor_cylinder'),
    path('qwikpartner-dashboard/cylinder/add-new', views.addQwikPartnerCylinder, name='qwikpartner_cylinder'),
    path('qwika-dashboard/products/update/<int:id>', views.updateProduct, name='qwikadmin_update_products'),
    path('qwika-dashboard/cylinders/update/<int:id>', views.updateCylinder, name='qwikadmin_update_cylinders'),
    path('qwika-dashboard/product/add-new', views.addProduct, name='qwikadmin_product'),
    path('qwika-dashboard/cylinder/add-new', views.addCylinder, name='qwikadmin_cylinder'),
    path('qwika-dashboard/products/delete/<int:id>', views.deleteProduct),
    path('qwika-dashboard/cylinders/delete/<int:id>', views.deleteCylinder),
    path('qwikpartner-dashboard/products/update/<int:id>', views.updateQwikPartnerProducts, name='update_products_partner'),
    # path('<id>/<slug>/', views.product_detail, name='product_detail'),
    # path('fund-wallet', views.fundWallet, name='fund'),
]
