from django import forms
#from django.contrib.gis import forms
from products.models import Product
from .models import UserOrder, OrderStatus, PayDelivery, PayLater, PaySmall
from django.forms.widgets import NumberInput
from django.core.exceptions import ValidationError
import datetime
#from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticMapWidget, GoogleStaticOverlayMapWidget

class UserOrderForm(forms.ModelForm):
    schedule_delivery = forms.DateField(label='Schedule Delivery', required=False, widget=NumberInput(attrs={'type': 'date'}))
    # address = forms.PointField(widget=GooglePointFieldWidget, required=False)

    # address = forms.PointField(widget=forms.OSMWidget(attrs={'map_width': 873,
    #                                                             'map_height': 270,
    #                                                             'default_lat': 6.5244,
    #                                                             'default_lon': 3.3792,
    #                                                             'default_zoom': 12}))

    # address = forms.CharField(widget= forms.TextInput
    #                       (attrs={'placeholder':'Leave blank if you wish to use registered address'}),
    #                       required = False)
    class Meta:
        model = UserOrder
        fields = ['outlet', 'address', 'schedule_delivery']
        # widgets = {
        #     'address': GooglePointFieldWidget,
        # }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['address'].label = 'Click location on the Map'

class UserOrderFormCust(forms.ModelForm):


    # address = forms.PointField(widget=forms.OSMWidget(attrs={'map_width': 1179,
    #                                                             'map_height': 270,
    #                                                             'default_zoom': 12}))

    # address = forms.CharField(widget= forms.TextInput
    #                       (attrs={'placeholder':'Leave blank if you wish to use registered address'}),
    #                       required = False)
    class Meta:
        model = UserOrder
        fields = ['outlet', 'address']

class ConfirmFormVendor(forms.ModelForm):
    PAID_CHOICES = [
        ('Confirmed', 'Confirmed')
    ]
    payment_status = forms.ChoiceField(label='Payment Status', choices=PAID_CHOICES)
    class Meta:
        model = UserOrder
        fields = ['payment_status']

class AddOrderFormVendor(forms.ModelForm):
    STATUS_CHOICES = [
        ('Out for Delivery','Out for Delivery'),
    ]
    # cylinder = forms.ModelMultipleChoiceField(queryset=Product.objects.filter(partner_product_status="Received Empty from QwikCustomer"))
    order_status = forms.ChoiceField(label='Select Present Order Status', choices=STATUS_CHOICES)
    class Meta:
        model = OrderStatus
        fields = ['order_status']

class AddOrderFormPartner(forms.ModelForm):
    STATUS_CHOICES = [
        ('Delivered','Delivered'),
    ]
    cylinder = forms.ModelMultipleChoiceField(queryset=Product.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_product_status="Unselected"))
    order_status = forms.ChoiceField(label='Select Present Order Status', choices=STATUS_CHOICES)
    class Meta:
        model = OrderStatus
        fields = ['cylinder', 'order_status']

class PayDeliveryForm(forms.ModelForm):
    PAYMENT_CHOICES = [
		('Bank Transfer','Bank Transfer'),
		('PoS', 'PoS'),
        ('Cash', 'Cash'),
	]
    payment_choice = forms.ChoiceField(label='Payment Choice', choices=PAYMENT_CHOICES, required = False)

    class Meta:
        model = PayDelivery
        fields = ['payment_choice']
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['state'].help_text = "Select from the available states we have for now"

class PayLaterForm(forms.ModelForm):
    PAYMENT_CHOICES = [
		('Bank Transfer','Bank Transfer'),
		('PoS', 'PoS'),
        ('Cash', 'Cash'),
	]
    payment_date_later = forms.DateField(label='Committed Payment Date', widget=NumberInput(attrs={'type': 'date'}), required = False)
    payment_choice = forms.ChoiceField(label='Payment Choice', choices=PAYMENT_CHOICES, required = False)

    class Meta:
        model = PayLater
        fields = ['payment_date_later', 'payment_choice']

class PaySmallForm(forms.ModelForm):
    PAYMENT_CHOICES = [
		('Bank Transfer','Bank Transfer'),
		('PoS', 'PoS'),
        ('Cash', 'Cash'),
	]
    payment1_date = forms.DateField(label='1st Payment Date', widget=NumberInput(attrs={'type': 'date'}), required = False)
    payment2_date = forms.DateField(label='2nd Payment Date', widget=NumberInput(attrs={'type': 'date'}), required = False)
    payment3_date = forms.DateField(label='3rd Payment Date', widget=NumberInput(attrs={'type': 'date'}), required = False)
    payment_choice = forms.ChoiceField(label='Payment Choice', choices=PAYMENT_CHOICES, required = False)

    class Meta:
        model = PaySmall
        fields = ['payment1_date', 'payment2_date', 'payment3_date', 'payment_choice']
        # fields = ['payment1', 'payment1_date', 'payment2', 'payment2_date', 'payment3', 'payment3_date', 'payment_choice']
