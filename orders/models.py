from django.db import models
from products.models import Product

class UserOrder(models.Model):
    PAID_CHOICES = [
        ('Unconfirmed', 'Unconfirmed'),
        ('Confirmed', 'Confirmed')
    ]
    user = models.ForeignKey('users.Person', null=True, blank=True, on_delete=models.SET_NULL)
    order_Id = models.CharField(max_length = 10, null=True)
    outlet = models.ForeignKey('users.Outlet', on_delete=models.SET_NULL, null=True, verbose_name="Select Our Outlet Closest to You")
    address = models.CharField(max_length = 255, blank=True, null=True, verbose_name="Delivery Address")
    schedule_delivery = models.DateField(blank=True, null=True, verbose_name="Schedule Delivery")
    payment_type = models.CharField(max_length=15, blank=True, null=True, verbose_name="Payment Type")
    payment_date_later = models.DateField(blank=True, null=True, verbose_name="Committed Payment Date")
    payment1 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="1st Payment")
    payment1_date = models.DateField(blank=True, null=True, verbose_name="1st Payment Date")
    payment2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="2nd Payment")
    payment2_date = models.DateField(blank=True, null=True, verbose_name="2nd Payment Date")
    payment3 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="3rd Payment")
    payment3_date = models.DateField(blank=True, null=True, verbose_name="3rd Payment Date")
    payment_choice = models.CharField(max_length=13, blank=True, null=True, verbose_name="Payment Choice")
    total_cost = models.DecimalField(max_digits=13, blank=True, null=True, decimal_places=2)
    payment_status = models.CharField(max_length=12, choices=PAID_CHOICES, default='Unconfirmed', null=True, verbose_name="Payment Status")
    user_order_status = models.CharField(max_length=11, default='Undelivered', null=True)
    point = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        try:
            return str(self.order_Id) + " | " + str(self.user.first_name) + " " + str(self.user.last_name)
        except:
            return str(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(UserOrder, on_delete=models.SET_NULL, null=True, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='items_products')
    order_item_status = models.CharField(max_length=16, default="New", null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(null=True, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        if self.price == None:
            pass
        else:
            return self.price * self.quantity

class OrderStatus(models.Model):
    STATUS_CHOICES = [
        ('Out for Delivery','Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ]
    order = models.ForeignKey(OrderItem, on_delete=models.SET_NULL, null=True, related_name='order_status')
    cylinder = models.ManyToManyField('products.Product', related_name='order_status_cylinders')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='order_status_products', verbose_name="Cylinder")
    order_status = models.CharField(max_length=30, choices=STATUS_CHOICES, null=True, verbose_name="Select Present Order Status")
    static_total_cost2 = models.DecimalField(max_digits=13, blank=True, null=True, decimal_places=2)
    employee = models.CharField(max_length=20, null=True, blank=True)
    who7_2 = models.CharField(max_length=9, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Order Status'
        verbose_name_plural = 'Order Statuses'

    def __str__(self):
        try:
            return str(self.order)
        except:
            return str(self.id)

class PayDelivery(models.Model):
    PAYMENT_CHOICES = [
		('Bank Transfer','Bank Transfer'),
		('PoS', 'PoS'),
        ('Cash', 'Cash'),
	]
    user = models.ForeignKey('users.Person', null=True, blank=True, on_delete=models.SET_NULL)
    pay_del_Id = models.CharField(max_length = 10, null=True)
    order = models.ForeignKey(UserOrder, on_delete=models.SET_NULL, null=True, related_name='order_delivery')
    payment_choice = models.CharField(max_length=13, choices=PAYMENT_CHOICES, null=True, verbose_name="Payment Choice")
    payment_ref = models.CharField(max_length=40, blank=True, null=True, verbose_name="Payment Reference (Bank Transfer)")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Pay on Delivery'
        verbose_name_plural = 'Pay on Deliveries'

    def __str__(self):
        try:
            return str(self.pay_del_Id)
        except:
            return str(self.id)

class PayLater(models.Model):
    PAYMENT_CHOICES = [
		('Bank Transfer','Bank Transfer'),
		('PoS', 'PoS'),
        ('Cash', 'Cash'),
	]
    user = models.ForeignKey('users.Person', null=True, blank=True, on_delete=models.SET_NULL)
    pay_lat_Id = models.CharField(max_length = 10, null=True)
    order = models.ForeignKey(UserOrder, on_delete=models.SET_NULL, null=True, related_name='order_later')
    payment_date_later = models.DateField(blank=True, null=True, verbose_name="Committed Payment Date")
    payment_choice = models.CharField(max_length=13, choices=PAYMENT_CHOICES, null=True, verbose_name="Payment Choice")
    payment_ref = models.CharField(max_length=40, blank=True, null=True, verbose_name="Payment Reference (Bank Transfer)")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        # verbose_name = 'Pay on Delivery'
        # verbose_name_plural = 'Pay os'

    def __str__(self):
        try:
            return str(self.pay_lat_Id)
        except:
            return str(self.id)

class PaySmall(models.Model):
    PAYMENT_CHOICES = [
		('Bank Transfer','Bank Transfer'),
		('PoS', 'PoS'),
        ('Cash', 'Cash'),
	]
    user = models.ForeignKey('users.Person', null=True, blank=True, on_delete=models.SET_NULL)
    pay_sma_Id = models.CharField(max_length = 10, null=True)
    order = models.ForeignKey(UserOrder, on_delete=models.SET_NULL, null=True, related_name='order_small')
    payment1 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="1st Payment")
    payment1_date = models.DateField(blank=True, null=True, verbose_name="1st Payment Date")
    payment2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="2nd Payment")
    payment2_date = models.DateField(blank=True, null=True, verbose_name="2nd Payment Date")
    payment3 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="3rd Payment")
    payment3_date = models.DateField(blank=True, null=True, verbose_name="3rd Payment Date")
    payment_choice = models.CharField(max_length=13, choices=PAYMENT_CHOICES, null=True, verbose_name="Payment Choice")
    payment_ref = models.CharField(max_length=40, blank=True, null=True, verbose_name="Payment Reference (Bank Transfer)")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        # verbose_name = 'Pay on Delivery'
        # verbose_name_plural = 'Pay os'

    def __str__(self):
        try:
            return str(self.pay_sma_Id)
        except:
            return str(self.id)
