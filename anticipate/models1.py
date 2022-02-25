from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.db import models
from products.models import Product

class AntiOrder(models.Model):
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
    TRANSACTION_CHOICES = [
		('Open','Open'),
		('Closed', 'Closed'),
	]
    user = models.ForeignKey('users.Person', null=True, blank=True, on_delete=models.SET_NULL)
    # order_Id = models.CharField(max_length = 10, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='anti_products')
    quantity = models.PositiveIntegerField(default=1)
    payment_type = models.CharField(max_length=15, choices=PAYMENT_TYPES, null=True, verbose_name="Payment Type")
    payment_date_later = models.DateField(blank=True, null=True, verbose_name="Commitment Payment Date (Paylater)")
    payment_split = models.CharField(max_length=40, blank=True, null=True, verbose_name="Payment Split in Amount (Pay Small Small)")
    payment_date_small = models.DateField(blank=True, null=True, verbose_name="Commitment Payment Date (Pay Small Small)")
    payment_choice = models.CharField(max_length=13, choices=PAYMENT_CHOICES, null=True, verbose_name="Payment Choice")
    payment_ref = models.CharField(max_length=40, blank=True, null=True, verbose_name="Payment Reference (Bank Transfer)")
    payment = models.CharField(max_length=16, blank=True, null=True)
    outlet = models.ForeignKey('users.Outlet', on_delete=models.SET_NULL, null=True, verbose_name="Select Our Outlet Closest to You")
    # address = models.PointField(null=True, verbose_name="Delivery Address")
    transaction = models.CharField(max_length=12, choices=TRANSACTION_CHOICES, default='Open', null=True, verbose_name="Transaction Status")
    # point = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{}'.format(self.id)

    def total_cost(self):
        if self.product.category.price == None:
            pass
        else:
            return self.product.category.price * self.quantity
