import django_filters as filters
from django_filters import CharFilter, DateFilter
from .models import UserOrder, OrderItem, OrderStatus
from django.forms.widgets import NumberInput
from django.db.models import Q

class UserOrderFilter(filters.FilterSet):
    start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    #created = DateFilter(label="Exact Date", input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Format: 1-1-2021 or 1/1/2021'}))

    class Meta:
        model = UserOrder
        fields = ['order_Id']

class UserOrderFilter2(filters.FilterSet):
    # address = CharFilter(field_name='address', lookup_expr='icontains', label="Address")
    start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    start_date3 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="schedule_delivery", lookup_expr='gte', label='Schedule Delivery', widget=NumberInput(attrs={'type': 'date'}))

    q = CharFilter(method='my_custom_filter',label="Others")

    class Meta:
        model = UserOrder
        fields = ['outlet']

    def __init__(self, *args, **kwargs):
        super(UserOrderFilter2, self).__init__(*args, **kwargs)
        self.filters['outlet'].label="Outlet"
    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(Q(user__username__icontains=value) | Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value) | Q(payment_type__icontains=value) | Q(payment_status__icontains=value) | Q(order_Id__icontains=value))

class UserOrderFilterSales(filters.FilterSet):
    # address = CharFilter(field_name='address', lookup_expr='icontains', label="Address")
    start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    # start_date3 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="schedule_delivery", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))

    q = CharFilter(method='my_custom_filter',label="Others")

    class Meta:
        model = UserOrder
        fields = ['outlet', 'payment_status']

    def __init__(self, *args, **kwargs):
        super(UserOrderFilterSales, self).__init__(*args, **kwargs)
        self.filters['outlet'].label="Outlet"
    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(Q(user__username__icontains=value) | Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value) | Q(payment_type__icontains=value) | Q(order_Id__icontains=value))

class UserOrderFilterPayments(filters.FilterSet):
    # address = CharFilter(field_name='address', lookup_expr='icontains', label="Address")
    start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    # start_date3 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="schedule_delivery", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))

    q = CharFilter(method='my_custom_filter',label="Others")

    class Meta:
        model = UserOrder
        fields = ['outlet']

    def __init__(self, *args, **kwargs):
        super(UserOrderFilterPayments, self).__init__(*args, **kwargs)
        self.filters['outlet'].label="Outlet"
    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(Q(user__username__icontains=value) | Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value) | Q(payment_type__icontains=value) | Q(order_Id__icontains=value))

class OrderItemFilter(filters.FilterSet):
    # outlet_o_static = CharFilter(field_name='outlet_o_static', lookup_expr='icontains', label="Outlet")
    start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    #created = DateFilter(label="Exact Date", input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'E.g. 1-1-2021'}))

    class Meta:
        model = OrderItem
        fields = ['order__order_Id', 'product__category']

    def __init__(self, *args, **kwargs):
        super(OrderItemFilter, self).__init__(*args, **kwargs)
        self.filters['order__order_Id'].label="Order Id"
        self.filters['product__category'].label="Product"

class OrderItemFilter2(filters.FilterSet):
    start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    #created = DateFilter(label="Exact Date", input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'E.g. 1-1-2021'}))

    class Meta:
        model = OrderItem
        fields = ['order__user', 'order__order_Id', 'product__category']

    def __init__(self, *args, **kwargs):
        super(OrderItemFilter2, self).__init__(*args, **kwargs)
        self.filters['order__user'].label="User"
        self.filters['order__order_Id'].label="Order Id"

class OrderStatusFilter(filters.FilterSet):
    #employee = CharFilter(field_name='employee', lookup_expr='icontains', label="Updated By")
    start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    # created = DateFilter(label="Exact Date", input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'E.g. 1-1-2021'}))

    class Meta:
        model = OrderStatus
        fields = ['order__order__order_Id', 'cylinder']

    def __init__(self, *args, **kwargs):
        super(OrderStatusFilter, self).__init__(*args, **kwargs)
        self.filters['order__order__order_Id'].label="Order Id"
        # self.filters['product'].label="Cylinder Id"

class OrderStatusFilter2(filters.FilterSet):
    #employee = CharFilter(field_name='employee', lookup_expr='icontains', label="Updated By")
    start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    # created = DateFilter(label="Exact Date", input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'E.g. 1-1-2021'}))

    class Meta:
        model = OrderStatus
        fields = ['order__order__user', 'order__order__order_Id', 'product', 'product__category']

    def __init__(self, *args, **kwargs):
        super(OrderStatusFilter2, self).__init__(*args, **kwargs)
        self.filters['order__order__user'].label="User"
        self.filters['order__order__order_Id'].label="Order Id"
        self.filters['product'].label="Cylinder Id"
        self.filters['product__category'].label="Product"
