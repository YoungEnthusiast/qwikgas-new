import django_filters as filters
from django_filters import DateFilter#, CharFilter
from .models import AntiOrder#, OrderItem, OrderStatus
from django.forms.widgets import NumberInput

class AntiOrderFilter(filters.FilterSet):
    start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    #created = DateFilter(label="Exact Date", input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Format: 1-1-2021 or 1/1/2021'}))

    class Meta:
        model = AntiOrder
        fields = []

class AntiOrderFilter2(filters.FilterSet):
    # address = CharFilter(field_name='address', lookup_expr='icontains', label="Address")
    start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    #created = DateFilter(label="Exact Date", input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'E.g. 1-1-2021'}))

    class Meta:
        model = AntiOrder
        fields = ['user']

    def __init__(self, *args, **kwargs):
        super(AntiOrderFilter2, self).__init__(*args, **kwargs)
