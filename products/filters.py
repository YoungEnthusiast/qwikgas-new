import django_filters as filters
from django_filters import CharFilter, DateFilter
from .models import Product, Category, Cylinder
from django.forms.widgets import TextInput

class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = ['type', 'mass', 'price']

class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = ['category', 'outlet', 'product_Id']

class CylinderFilter(filters.FilterSet):
    Cylinder = CharFilter(field_name='cylinder__product_Id', lookup_expr='icontains', label="Cylinder ID")
    class Meta:
        model = Cylinder
        fields = []
        # fields = ['cylinder', 'vendor_product_status', 'partner_product_status', 'customer_product_status', 'admin_product_status']
    # def __init__(self, *args, **kwargs):
    #     super(CylinderFilter, self).__init__(*args, **kwargs)
    #     self.filters['vendor_product_status'].label="Vendor's Remark"
    #     self.filters['partner_product_status'].label="Partner's Remark"


class ProductFilterAdmin(filters.FilterSet):
    class Meta:
        model = Product
        fields = ['category', 'outlet', 'product_Id', 'vendor_product_status']
