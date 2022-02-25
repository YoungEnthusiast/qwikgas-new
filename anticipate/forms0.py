from django import forms
from .models import AntiOrder#, VisitorOrder, OrderStatus
from django.forms.widgets import NumberInput
from django.core.exceptions import ValidationError
import datetime

class AntiOrderForm(forms.ModelForm):
    PAYMENT_TYPES = [
		('Payment Now','Payment Now'),
		('Paylater', 'Paylater'),
        ('Pay Small Small', 'Pay Small Small'),
	]
    PAYMENT_CHOICES = [
		('Bank Transfer','Bank Transfer'),
		('PoS', 'PoS'),
        ('Cash', 'Cash'),
	]
    payment_type = forms.ChoiceField(label='Payment Type', choices=PAYMENT_TYPES, widget=forms.RadioSelect)
    payment_choice = forms.ChoiceField(label='Payment Choice', choices=PAYMENT_CHOICES)
    payment_date_later = forms.DateField(label='Commitment Payment Date (Paylater)', widget=NumberInput(attrs={'type': 'date'}))
    payment_date_small = forms.DateField(label='Commitment Payment Date (Pay Small Small)', widget=NumberInput(attrs={'type': 'date'}))


    # address = forms.CharField(widget= forms.TextInput
    #                       (attrs={'placeholder':'Leave blank if you wish to use registered address'}),
    #                       required = False)

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
# payment_date_later = models.DateField(blank=True, null=True, verbose_name="Commitment Payment Date (Paylater)")
# payment_split = models.CharField(max_length=40, blank=True, null=True, verbose_name="Payment Split in Amount (Pay Small Small)")
# payment_date_small = models.DateField(blank=True, null=True, verbose_name="Commitment Payment Date (Pay Small Small)")
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
