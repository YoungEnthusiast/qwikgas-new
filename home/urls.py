from django.urls import path
from . import views

urlpatterns = [
    path('', views.showHome, name='index'),
    path('gallery', views.showGallery, name='gallery'),
    path('about-us', views.showAbout, name='about'),
    path('contact-us', views.showContact, name='contact'),
]
