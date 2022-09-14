from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    type = models.CharField(max_length=20, db_index=True, unique=True, verbose_name="Product Type")
    mass = models.CharField(max_length=6, db_index=True, unique=True, verbose_name="LPG Weight")
    slug = models.SlugField(max_length=200, db_index=True)
    price = models.DecimalField(max_digits=11, null=True, decimal_places=2)
    tare = models.CharField(max_length=6, db_index=True, unique=True, null=True, verbose_name="Tare Weight")
    working = models.CharField(max_length=6, db_index=True, null=True, verbose_name="Working Pressure")
    test = models.CharField(max_length=6, db_index=True, null=True, verbose_name="Test Pressure")
    water = models.CharField(max_length=6, db_index=True, null=True, verbose_name="Water Capacity")
    image = models.ImageField(upload_to='categories_img/%Y/%m/%d', null=True, blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('type',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return str(self.type)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug])

class Product(models.Model):
    VENDOR_CHOICES = [
        ('Dispatched to Plant','Dispatched to Plant'),
        ('Released Filled to QwikPartner', 'Released Filled to QwikPartner'),

        ('Dispatched Empty','Dispatched Empty'),
        ('Received Empty', 'Received Empty'),
        ('Dispatched Filled','Dispatched Filled'),
        ('Received Filled', 'Received Filled'),
    ]
    PARTNER_CHOICES = [
        ('Received Empty from QwikCustomer', 'Received Empty from QwikCustomer'),
        ('Returned Empty','Returned Empty'),
        ('Received Empty', 'Received Empty'),
        ('Received Filled', 'Received Filled'),

        ('Selected', 'Selected'),
        ('Unselected', 'Unselected'),
    ]
    CUSTOMER_CHOICES = [
        ('Returned Empty to QwikPartner','Returned Empty to QwikPartner'),
        ('Received Filled', 'Received Filled'),
    ]
    ADMIN_CHOICES = [
        ('Received Empty from QwikCustomer', 'Received Empty from QwikCustomer'),
        ('Returned Empty to QwikLet','Returned Empty to QwikLet'),
        ('Dispatched to Plant', 'Dispatched to Plant'),
        ('Delivered Filled to QwikLet', 'Delivered Filled to QwikLet'),
        ('Dispatched Filled to QwikCustomer', 'Dispatched Filled to QwikCustomer'),
        ('Delivered to QwikCustomer', 'Delivered to QwikCustomer'),
        ('Returned Filled to QwikLet', 'Returned Filled to QwikLet'),
    ]
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products_category', verbose_name="Product")
    product_Id = models.CharField(max_length=20, null=True, unique=True, verbose_name="Cylinder Id")
    available = models.BooleanField(max_length=5, default = False)
    outlet = models.ForeignKey('users.Outlet', on_delete=models.SET_NULL, null=True)
    vendor_product_status = models.CharField(max_length=30, choices=VENDOR_CHOICES, null=True, verbose_name="QwikVendor's Remark")
    vendor_product = models.CharField(max_length=20, null=True, blank=True)
    vendor_consent = models.BooleanField(max_length=5, default = False)
    partner_product_status = models.CharField(max_length=35, choices=PARTNER_CHOICES, default="Unselected", blank=True, null=True, verbose_name="QwikPartner's Remark")
    partner_product = models.CharField(max_length=20, null=True, blank=True)
    partner_consent = models.BooleanField(max_length=5, default = False)
    batch_Id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('product_Id',)
        index_together = (('id',))
    def __str__(self):
        try:
            return str(self.product_Id)
        except:
            return str(self.id)

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id])

    def get_absolute_url2(self):
        return reverse('products:product_detail2', args=[self.id])

class Cylinder(models.Model):
    VENDOR_CHOICES = [
        ('Dispatched to Plant','Dispatched to Plant'),
        ('Returned Empty to QwikLet', 'Returned Empty to QwikLet'),
        ('Delivered Filled to QwikLet', 'Delivered Filled to QwikLet'),
        ('Released Filled to QwikPartner', 'Released Filled to QwikPartner'),
        ('Delivered to QwikCustomer', 'Delivered to QwikCustomer'),
        ('Returned Filled to QwikLet', 'Returned Filled to QwikLet'),
        ('Delivered to QwikCustomer', 'Delivered to QwikCustomer'),

    ]
    PARTNER_CHOICES = [
        ('Received Empty from QwikCustomer', 'Received Empty from QwikCustomer'),
        ('Returned Empty to QwikLet','Returned Empty to QwikLet'),
        ('Dispatched to Plant', 'Dispatched to Plant'),
        ('Delivered Filled to QwikLet', 'Delivered Filled to QwikLet'),
        ('Dispatched Filled to QwikCustomer', 'Dispatched Filled to QwikCustomer'),
        ('Delivered to QwikCustomer', 'Delivered to QwikCustomer'),
        ('Returned Filled to QwikLet', 'Returned Filled to QwikLet'),
    ]
    # CONFIRMS = [
    #     ('Accept', 'Accept'),
    #     ('Decline', 'Decline'),
    # ]

    CUSTOMER_CHOICES = [
        ('Returned Empty to QwikPartner','Returned Empty to QwikPartner'),
        ('Received Filled', 'Received Filled'),
    ]
    ADMIN_CHOICES = [
        ('Received Empty from QwikCustomer', 'Received Empty from QwikCustomer'),
        ('Returned Empty to QwikLet','Returned Empty to QwikLet'),
        ('Dispatched to Plant', 'Dispatched to Plant'),
        ('Delivered Filled to QwikLet', 'Delivered Filled to QwikLet'),
        ('Dispatched Filled to QwikCustomer', 'Dispatched Filled to QwikCustomer'),
        ('Delivered to QwikCustomer', 'Delivered to QwikCustomer'),
        ('Returned Filled to QwikLet', 'Returned Filled to QwikLet'),
    ]
    cylinder = models.CharField(max_length=30, null=True, verbose_name="Cylinder Id")
    category = models.CharField(max_length=12, null=True)
    outlet = models.CharField(max_length=30, null=True)
    # cylinder = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, verbose_name="Cylinder Id")
    customer = models.ForeignKey('users.Person', null=True, blank=True, on_delete=models.SET_NULL)
    vendor_product_status = models.CharField(max_length=30, choices=VENDOR_CHOICES, null=True, verbose_name="QwikVendor's Remark")
    partner_product_status = models.CharField(max_length=35, choices=PARTNER_CHOICES, blank=True, null=True, verbose_name="QwikPartner's Remark")
    partner_confirm = models.BooleanField(blank=True, null=True, verbose_name="QwikPartner's Confirmation")
    vendor_confirm = models.BooleanField(blank=True, null=True, default=False, verbose_name="QwikVendor's Confirmation")
    who = models.CharField(max_length=8, blank=True, null=True)
    who_2 = models.CharField(max_length=9, blank=True, null=True)
    who2 = models.CharField(max_length=8, blank=True, null=True)
    who2_2 = models.CharField(max_length=9, blank=True, null=True)
    who3 = models.CharField(max_length=8, blank=True, null=True)
    who3_2 = models.CharField(max_length=9, blank=True, null=True)
    who4 = models.CharField(max_length=8, blank=True, null=True)
    who4_2 = models.CharField(max_length=9, blank=True, null=True)
    who5 = models.CharField(max_length=8, blank=True, null=True)
    who5_2 = models.CharField(max_length=9, blank=True, null=True)
    who8 = models.CharField(max_length=19, blank=True, null=True)
    who8_1 = models.CharField(max_length=8, blank=True, null=True)
    who8_2 = models.CharField(max_length=9, blank=True, null=True)
    customer_product_status = models.CharField(max_length=35, choices=CUSTOMER_CHOICES, blank=True, null=True, verbose_name="QwikCustomer's Remark")
    admin_product_status = models.CharField(max_length=35, choices=ADMIN_CHOICES, blank=True, null=True, verbose_name="QwikAdmin's Remark")
    admin_product = models.CharField(max_length=20, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        index_together = (('id',))
    def __str__(self):
        try:
            return str(self.cylinder)
        except:
            return str(self.id)

class Owing(models.Model):
    cylinder = models.CharField(max_length=110, null=True, verbose_name="Cylinder Id")
    category = models.CharField(max_length=12, null=True)
    outlet = models.CharField(max_length=30, null=True)
    customer = models.ForeignKey('users.Person', null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        index_together = (('id',))
    def __str__(self):
        try:
            return str(self.cylinder)
        except:
            return str(self.id)
