import django_filters as filters
from django_filters import CharFilter, DateFilter
from .models import Person, Wallet, Outlet
from django.forms.widgets import NumberInput

# from django.db.models import Q
# import django_filters
#
#
# class LocationFilter(django_filters.FilterSet):
#     q = django_filters.CharFilter(method='my_custom_filter',label="Search")
#
#     class Meta:
#         model = Location
#         fields = ['q']
#
#     def my_custom_filter(self, queryset, name, value):
#         return queryset.filter(
#             Q(loc__icontains=value) | Q(loc_mansioned__icontains=value) | Q(loc_country__icontains=value) | Q(loc_modern__icontains=value)
#         )

class WalletFilter(filters.FilterSet):
    transaction_type = CharFilter(field_name='transaction_type', lookup_expr='icontains', label="Transaction Type")
    # dob = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), required=False)
    start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    # created = DateFilter(label="Exact Date", input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Format: 1-1-2021 or 1/1/2021'}))


    class Meta:
        model = Wallet
        fields = ['transaction_type']

    # def __init__(self, *args, **kwargs):
    #     super(WalletFilter, self).__init__(*args, **kwargs)
    #     self.filters['amount_debited'].label="Debit"
    #     self.filters['amount_credited'].label="Credit"

class WalletFilter2(filters.FilterSet):
    start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    created = DateFilter(label="Exact Date", input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], lookup_expr='icontains', widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = Wallet
        fields = ['user', 'transaction_type', 'amount_debited', 'amount_credited']

class PeopleFilter(filters.FilterSet):
    first_name = CharFilter(field_name='first_name', lookup_expr='icontains', label="First Name")
    last_name = CharFilter(field_name='first_name', lookup_expr='icontains', label="Last Name")
    phone_number = CharFilter(field_name='phone_number', lookup_expr='icontains', label="Phone Number")
    address = CharFilter(field_name='address', lookup_expr='icontains', label="Address")
    referrer = CharFilter(field_name='referrer', lookup_expr='icontains', label="Referrer's Username")
    class Meta:
        model = Person
        fields = ['username', 'type', 'outlet']

    def __init__(self, *args, **kwargs):
        super(PeopleFilter, self).__init__(*args, **kwargs)
        self.filters['type'].label="User Type"
        self.filters['outlet'].label="Outlet"

class OutletFilter(filters.FilterSet):
    class Meta:
        model = Outlet
        fields = ['manager', 'outlet']
