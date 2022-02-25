from django import forms
# from django.contrib.gis import forms
from django.core.exceptions import ValidationError
from orders.models import OrderItem
# from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticMapWidget, GoogleStaticOverlayMapWidget

#PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 501)]


# class CartAddProductForm(forms.Form):
#     # quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
#     #                                   coerce=int)
#
#     quantity = forms.IntegerField(label="How many?")
#     outlet_o = forms.CharField(label="Select Outlet")
#     address_o = forms.CharField(label="Address")
#     update = forms.BooleanField(required=False,
#                                 initial=False,
#                                 widget=forms.HiddenInput)
#
#     def clean_quantity(self):
#         if self.cleaned_data.get('quantity') < 1:
#             raise ValidationError("You cannot order less than 1")
#         return self.cleaned_data.get('quantity')


class CartAddProductForm(forms.ModelForm):
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)


    def clean_quantity(self):
        if self.cleaned_data.get('quantity') < 1:
            raise ValidationError("You cannot order less than 1")
        return self.cleaned_data.get('quantity')
    class Meta:
        model = OrderItem
        fields = ['quantity']
