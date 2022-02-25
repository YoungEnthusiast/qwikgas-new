from django import forms
from .models import Contact
from django.core import validators
# from .models import City
#from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticMapWidget, GoogleStaticOverlayMapWidget

class ContactForm(forms.ModelForm):
    phone_number = forms.CharField(label='Phone Number')
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone_number', 'message']

#
# class CityCreateForm(forms.ModelForm):
#
#     class Meta:
#         model = City
#         fields = ('name', 'location')
#         widgets = {
#             'location': GooglePointFieldWidget,
#         }
#
#
# class CityDetailForm(forms.ModelForm):
#
#     class Meta:
#         model = City
#         fields = ('name', 'location')
#         widgets = {
#             'location': GoogleStaticOverlayMapWidget(zoom=12, thumbnail_size='50x50', size='640x640'),
#         }
