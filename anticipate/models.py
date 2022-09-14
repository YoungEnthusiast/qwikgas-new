from django.db import models
from products.models import Product
from users.models import Person

class AntiOrder(models.Model):
    PAYMENT_TYPE1 = [
		('Pay Now','Pay Now'),
	]
    PAYMENT_TYPE2 = [
		('Paylater', 'Paylater'),
	]
    PAYMENT_TYPE3 = [
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
    user = models.ForeignKey(Person, null=True, blank=True, on_delete=models.SET_NULL)
    order_Id = models.IntegerField(blank=True, null=True)
    cylinder = models.ManyToManyField('products.Product', related_name='anti_cylinders')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, related_name='anti_products')
    category = models.CharField(max_length=12, blank=True, null=True)
    outlet_static = models.CharField(max_length=30, blank=True, null=True)
    who6_2 = models.CharField(max_length=9, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    payment_type1 = models.CharField(max_length=7, choices=PAYMENT_TYPE1, blank=True, null=True, verbose_name="Payment Type")
    payment_type2 = models.CharField(max_length=8, choices=PAYMENT_TYPE2, blank=True, null=True, verbose_name="")
    payment_type3 = models.CharField(max_length=15, choices=PAYMENT_TYPE3, blank=True, null=True, verbose_name="")
    payment_date_later = models.DateField(blank=True, null=True, verbose_name="Committed Payment Date")
    payment_split = models.CharField(max_length=40, blank=True, null=True, verbose_name="Payment Split in Amount")
    # payment_date_small = models.DateField(blank=True, null=True, verbose_name="Committed Payment Date")
    payment_choice = models.CharField(max_length=13, choices=PAYMENT_CHOICES, null=True, verbose_name="Payment Choice")
    payment_ref = models.CharField(max_length=40, blank=True, null=True, verbose_name="Payment Reference")
    payment1 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True, verbose_name="1st Payment")
    payment1_date = models.DateField(blank=True, null=True, verbose_name="1st Payment Date")
    payment2 = models.DecimalField(max_digits=10,  decimal_places=2, blank=True, null=True, verbose_name="2nd Payment")
    payment2_date = models.DateField(blank=True, null=True, verbose_name="2nd Payment Date")
    payment3 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="3rd Payment")
    payment3_date = models.DateField(blank=True, null=True, verbose_name="3rd Payment Date")
    payment_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    outlet = models.ForeignKey('users.Outlet', on_delete=models.SET_NULL, null=True, blank=True)
    stage = models.CharField(max_length=3, blank=True, null=True)
    transaction = models.CharField(max_length=12, choices=TRANSACTION_CHOICES, default='Open', blank=True, null=True, verbose_name="Transaction Status")


    static_price = models.DecimalField(max_digits=11, blank=True, null=True, decimal_places=2)
    static_total_cost = models.DecimalField(max_digits=13, default=0, blank=True, null=True, decimal_places=2)
    static_price2 = models.DecimalField(max_digits=11, blank=True, null=True, decimal_places=2)
    static_total_cost2 = models.DecimalField(max_digits=13, blank=True, null=True, decimal_places=2)
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
