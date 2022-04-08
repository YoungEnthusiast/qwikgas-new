from django import forms
from users.models import Person
from orders.models import OrderStatus
from .models import Product, Category, Cylinder
from anticipate.models import AntiOrder
from django.core.exceptions import ValidationError

class CylinderFormVendor(forms.ModelForm):
    class Meta:
        model = Cylinder
        fields = ['cylinder']

class CylinderFormPartner(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Person.objects.filter(type="QwikCustomer"))
    # cylinder = forms.ModelChoiceField(queryset=Cylinder.objects.filter(partner_product_status="Delivered to QwikCustomer"))
    class Meta:
        model = Cylinder
        fields = ['customer', 'cylinder']

class CylinderFormCustomerUp(forms.ModelForm):
    class Meta:
        model = Cylinder
        fields = ['customer_product_status']

class CylinderFormVendorUp(forms.ModelForm):
    class Meta:
        model = Cylinder
        fields = ['vendor_product_status']

class CylinderFormPartnerUp(forms.ModelForm):
    class Meta:
        model = Cylinder
        fields = ['partner_product_status']

class CylinderFormAdminUp(forms.ModelForm):
    class Meta:
        model = Cylinder
        fields = ['cylinder', 'customer']

class CylinderFormAdminUpDispatchedToPlant(forms.ModelForm):
    class Meta:
        model = Cylinder
        fields = ['cylinder']

class CylinderFormAdminUpReturnedFilledToQwikLet(forms.ModelForm):
    class Meta:
        model = Cylinder
        fields = ['cylinder']

class CylinderFormAdminUpDispatchedToQwikCustomer(forms.ModelForm):
    class Meta:
        model = Cylinder
        fields = ['cylinder']

class CylinderFormAdminUpDeliveredToQwikCustomerAnti(forms.ModelForm):
    class Meta:
        model = AntiOrder
        fields = ['user', 'product']

class CylinderFormAdminUpDeliveredToQwikCustomerUser(forms.ModelForm):
    class Meta:
        model = OrderStatus
        fields = ['product']

# class CylinderFormAdminUpReturnedEmpty(forms.ModelForm):
#     vendor_confirm = forms.BooleanField()
#     class Meta:
#         model = Cylinder
#         fields = ['vendor_confirm']

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['category'].required = False
            self.fields['category'].widget.attrs['disabled'] = 'disabled'
            self.fields['product_Id'].required = False
            self.fields['product_Id'].widget.attrs['disabled'] = 'disabled'
            self.fields['outlet'].required = False
            self.fields['outlet'].widget.attrs['disabled'] = 'disabled'

    def clean_category(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.category
        else:
            return self.cleaned_data.get('category', None)

    def clean_product_Id(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.product_Id
        else:
            return self.cleaned_data.get('product_Id', None)

    def clean_outlet(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.outlet
        else:
            return self.cleaned_data.get('outlet', None)

    class Meta:
        model = Product
        fields = ['category', 'product_Id', 'outlet', 'vendor_product_status']

class ProductFormPartner(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductFormPartner, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['category'].required = False
            self.fields['category'].widget.attrs['disabled'] = 'disabled'
            self.fields['product_Id'].required = False
            self.fields['product_Id'].widget.attrs['disabled'] = 'disabled'
            self.fields['outlet'].required = False
            self.fields['outlet'].widget.attrs['disabled'] = 'disabled'
            self.fields['vendor_product_status'].required = False
            self.fields['vendor_product_status'].widget.attrs['disabled'] = 'disabled'

    def clean_category(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.category
        else:
            return self.cleaned_data.get('category', None)

    def clean_product_Id(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.product_Id
        else:
            return self.cleaned_data.get('product_Id', None)

    def clean_outlet(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.outlet
        else:
            return self.cleaned_data.get('outlet', None)

    def clean_vendor_product_status(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.vendor_product_status
        else:
            return self.cleaned_data.get('vendor_product_status', None)

    class Meta:
        model = Product
        fields = ['category', 'product_Id', 'outlet', 'vendor_product_status', 'partner_product_status']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['type', 'mass', 'price', 'image', 'description', 'tare', 'water', 'test', 'working']

class ProductFormAdmin(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'product_Id', 'outlet', 'vendor_product_status', 'batch_Id']
