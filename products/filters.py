import django_filters as filters
from django_filters import CharFilter, DateFilter
from .models import Product, Category, Cylinder
from django.forms.widgets import TextInput, NumberInput
from django.db.models import Q

class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = ['type', 'mass', 'price']

class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = ['category', 'outlet', 'product_Id']

class CylinderFilter(filters.FilterSet):
    start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    # customer_id = CharFilter(field_name='customer__username', lookup_expr='icontains', label="Customer's ID")
    q = CharFilter(method='my_custom_filter',label="Others")
    class Meta:
        model = Cylinder
        fields = []
    # def __init__(self, *args, **kwargs):
    #     super(CylinderFilter, self).__init__(*args, **kwargs)
    #     self.filters['vendor_product_status'].label="Vendor's Remark"
    #     self.filters['partner_product_status'].label="Partner's Remark"
    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(Q(customer__username__icontains=value) | Q(customer__first_name__icontains=value) | Q(customer__last_name__icontains=value) | Q(outlet__icontains=value) | Q(category__icontains=value )| Q(cylinder__icontains=value))

class CylinderFilter2(filters.FilterSet):
    start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    # customer_id = CharFilter(field_name='customer__username', lookup_expr='icontains', label="Customer's ID")
    q = CharFilter(method='my_custom_filter',label="Others")
    class Meta:
        model = Cylinder
        fields = []
    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(Q(customer__username__icontains=value) | Q(customer__first_name__icontains=value) | Q(customer__last_name__icontains=value) | Q(outlet__icontains=value) | Q(category__icontains=value )| Q(cylinder__icontains=value))

class CylinderFilter3(filters.FilterSet):
    start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    # customer_id = CharFilter(field_name='customer__username', lookup_expr='icontains', label="Customer's ID")
    q = CharFilter(method='my_custom_filter',label="Others")
    class Meta:
        model = Cylinder
        fields = []
    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(Q(category__icontains=value )| Q(outlet__icontains=value) | Q(cylinder__icontains=value))

class ProductFilterAdmin(filters.FilterSet):
    class Meta:
        model = Product
        fields = ['category', 'outlet', 'product_Id', 'vendor_product_status']
