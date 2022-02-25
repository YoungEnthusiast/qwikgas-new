from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('adm/', admin.site.urls),
    path('', include('home.urls')),
    # path('', include('pictures.urls')),
    # path('', include('videos.urls')),
    # path('', include('news.urls')),
    # path('', include('articles.urls')),
    path('', include('users.urls')),
    path('', include(('products.urls', 'products'), namespace='products')),
    path('cart', include(('cart.urls', 'cart'), namespace='cart')),
    path('', include(('orders.urls', 'orders'), namespace='orders')),
    path('', include(('anticipate.urls', 'anticipate'), namespace='anticipate')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)
