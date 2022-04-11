from django import forms
from users.models import Person
from .models import AntiOrder#, VisitorOrder, OrderStatus
from products.models import Cylinder, Product
from django.forms.widgets import NumberInput
from django.core.exceptions import ValidationError
import datetime

class AntiOrderForm(forms.ModelForm):
    PAYMENT_TYPE1 = [
		('Pay Now','Pay Now'),
	]
    PAYMENT_TYPE2 = [
		('Paylater', 'Paylater'),
	]
    PAYMENT_TYPE3 = [
        ('Pay Small Small', 'Pay Small Small'),
	]
    PAYMENT_CHOICES = [
		('Bank Transfer','Bank Transfer'),
		('PoS', 'PoS'),
        ('Cash', 'Cash'),
	]
    cylinder = forms.ModelMultipleChoiceField(queryset=Product.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_product_status="Unselected"))
    user = forms.ModelChoiceField(queryset=Person.objects.filter(type="QwikCustomer"))
    payment_type1 = forms.ChoiceField(label='Payment Type', choices=PAYMENT_TYPE1, widget=forms.RadioSelect, required = False)
    payment_type2 = forms.ChoiceField(label='', choices=PAYMENT_TYPE2, widget=forms.RadioSelect, required = False)
    payment_type3 = forms.ChoiceField(label='', choices=PAYMENT_TYPE3, widget=forms.RadioSelect, required = False)
    payment_choice = forms.ChoiceField(label='Payment Choice', choices=PAYMENT_CHOICES, required = False)
    payment_date_later = forms.DateField(label='Committed Payment Date', widget=NumberInput(attrs={'type': 'date'}), required = False)
    payment1_date = forms.DateField(label='1st Payment Date', widget=NumberInput(attrs={'type': 'date'}), required = False)
    payment2_date = forms.DateField(label='2nd Payment Date', widget=NumberInput(attrs={'type': 'date'}), required = False)
    payment3_date = forms.DateField(label='3rd Payment Date', widget=NumberInput(attrs={'type': 'date'}), required = False)

    def clean_state(self):
        state = self.cleaned_data.get('state')
        if state == "Select a State":
            raise ValidationError("Please select a state from the dropdown")
        return state

    def clean_schedule_Delivery(self):
       schedule_Delivery = self.cleaned_data.get('schedule_Delivery')
       if schedule_Delivery < datetime.date.today() + datetime.timedelta(days=2):
           raise ValidationError("You cannot schedule within less than 48 hours")
       return schedule_Delivery

# user = models.ForeignKey('users.Person', null=True, blank=True, on_delete=models.SET_NULL)
# # order_Id = models.CharField(max_length = 10, null=True)
# product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='anti_products')
# quantity = models.PositiveIntegerField(default=1)
# payment_type = models.CharField(max_length=15, choices=PAYMENT_TYPES, null=True, verbose_name="Payment Type")
# payment_date_later = models.DateField(blank=True, null=True, verbose_name="Committed Payment Date (Paylater)")
# payment_split = models.CharField(max_length=40, blank=True, null=True, verbose_name="Payment Split in Amount (Pay Small Small)")
# payment_date_small = models.DateField(blank=True, null=True, verbose_name="Committed Payment Date (Pay Small Small)")
# payment_choice = models.CharField(max_length=13, choices=PAYMENT_CHOICES, null=True, verbose_name="Payment Choice")
# payment_ref = models.CharField(max_length=40, blank=True, null=True, verbose_name="Payment Reference (Bank Transfer)")
#
# outlet = models.ForeignKey('users.Outlet', on_delete=models.SET_NULL, null=True, verbose_name="Select Our Outlet Closest to You")
# # address = models.PointField(null=True, verbose_name="Delivery Address")
# transaction = models.CharField(max_length=12, choices=TRANSACTION_CHOICES, default='Open', null=True, verbose_name="Transaction Status")
# # point = models.PositiveIntegerField(default=0)
# created = models.DateTimeField(auto_now_add=True)
# updated = models.DateTimeField(auto_now=True)

    class Meta:
        model = AntiOrder
        fields = '__all__'
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['state'].help_text = "Select from the available states we have for now"

class AntiOrderFormVen(forms.ModelForm):
    class Meta:
        model = AntiOrder
        fields = ['transaction']
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['state'].help_text = "Select from the available states we have for now"

class AntiOrderFormPar(forms.ModelForm):
    payment2_date = forms.DateField(label='Date', widget=NumberInput(attrs={'type': 'date'}), required = False)
    class Meta:
        model = AntiOrder
        fields = ['payment2', 'payment2_date']

class AntiOrderFormPar2(forms.ModelForm):
    payment3_date = forms.DateField(label='Date', widget=NumberInput(attrs={'type': 'date'}), required = False)
    class Meta:
        model = AntiOrder
        fields = ['payment3', 'payment3_date']
