import django_filters as filters
from django_filters import DateFilter, CharFilter
from .models import AntiOrder#, OrderItem, OrderStatus
from django.forms.widgets import NumberInput
from django.db.models import Q

class AntiOrderFilter(filters.FilterSet):
    start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    #created = DateFilter(label="Exact Date", input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Format: 1-1-2021 or 1/1/2021'}))

    class Meta:
        model = AntiOrder
        fields = []

class AntiOrderFilter2(filters.FilterSet):
    start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    q = CharFilter(method='my_custom_filter',label="Others")

    class Meta:
        model = AntiOrder
        fields = ['outlet', 'cylinder']
    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(Q(user__username__icontains=value) | Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value) | Q(payment_choice__icontains=value) | Q(payment_type1__icontains=value) | Q(payment_type2__icontains=value) | Q(payment_type3__icontains=value) | Q(transaction__icontains=value))

class AntiOrderFilterSales(filters.FilterSet):
    start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    q = CharFilter(method='my_custom_filter',label="Others")

    class Meta:
        model = AntiOrder
        fields = ['outlet', 'transaction']
    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(Q(user__username__icontains=value) | Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value) | Q(payment_choice__icontains=value) | Q(payment_type1__icontains=value) | Q(payment_type2__icontains=value) | Q(payment_type3__icontains=value))

class AntiOrderFilterCredits(filters.FilterSet):
    start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    q = CharFilter(method='my_custom_filter',label="Others")

    class Meta:
        model = AntiOrder
        fields = ['outlet', 'transaction']
    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(Q(user__username__icontains=value) | Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value) | Q(payment_choice__icontains=value) | Q(payment_type1__icontains=value) | Q(payment_type2__icontains=value) | Q(payment_type3__icontains=value))

class AntiOrderFilterPayments(filters.FilterSet):
    start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    q = CharFilter(method='my_custom_filter',label="Others")

    class Meta:
        model = AntiOrder
        fields = ['outlet']
    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(Q(user__username__icontains=value) | Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value) | Q(payment_choice__icontains=value) | Q(payment_type1__icontains=value) | Q(payment_type2__icontains=value) | Q(payment_type3__icontains=value) | Q(payment_total__icontains=value))
