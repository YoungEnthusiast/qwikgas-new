from django.db import models
from django.contrib.auth.models import AbstractUser

class Vendor(models.Model):
    person = models.ForeignKey('users.Person', on_delete=models.SET_NULL, null=True, related_name="vendor")

class Partner(models.Model):
    person = models.ForeignKey('users.Person', on_delete=models.SET_NULL, null=True, related_name="partner")

class Admin(models.Model):
    person = models.ForeignKey('users.Person', on_delete=models.SET_NULL, null=True, related_name="admin")

class State(models.Model):
    state = models.CharField(max_length=20, unique=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        try:
            return str(self.state)
        except:
            return str(self.id)

class Lg(models.Model):
    lg = models.CharField(max_length=20, unique=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        try:
            return str(self.lg)
        except:
            return str(self.id)

class Outlet(models.Model):
    manager = models.ForeignKey('users.Person', on_delete=models.SET_NULL, null=True, related_name="outlet_manager")
    partner = models.ForeignKey('users.Person', on_delete=models.SET_NULL, null=True, related_name="outlet_partner")
    outlet = models.CharField(max_length=20, unique=True, null=True)
    address = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=100, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        try:
            return str(self.outlet)
        except:
            return str(self.id)


class Person(AbstractUser):
    GENDER_CHOICES = [
		('Male','Male'),
		('Female', 'Female')
	]
    TYPE_CHOICES = [
        ('QwikCustomer', 'QwikCustomer'),
		('QwikVendor', 'QwikVendor'),
        ('QwikPartner', 'QwikPartner'),
        ('QwikA--', 'QwikA--'),
    ]
    com_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Company/Business Name")
    phone_number = models.CharField(max_length=20, null=True, verbose_name="Phone Number")
    address = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    dob = models.DateField(blank=True, null=True, verbose_name="Date of Start of Business")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='QwikCustomer', blank=True, null=True)
    photograph = models.ImageField(upload_to='users_img/%Y/%m/%d', null=True, blank=True)
    holding = models.CharField(max_length=15, blank=True, null=True)
    state = models.ForeignKey('users.State', on_delete=models.SET_NULL, blank=True, null=True)
    lg = models.ForeignKey('users.Lg', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="LG")
    city = models.CharField(max_length=20, blank=True, null=True)
    outlet = models.ForeignKey('users.Outlet', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Select Our Outlet Closest to You")
    about_me = models.TextField(max_length=255, blank=True, null=True, verbose_name="About Me")
    referrer = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Person'
        verbose_name_plural = 'People'

    def __str__(self):
        try:
            return str(self.username) + " | " + str(self.first_name) + " " + str(self.last_name)
        except:
            return str(self.id)

    @property
    def photographURL(self):
        try:
            url = self.photograph.url
        except:
            url = ''
        return url

    def age(self):
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

class Wallet(models.Model):
    user = models.ForeignKey('users.Person', on_delete = models.SET_NULL, null=True)
    transaction_type = models.CharField(max_length=12, blank=True, null=True, verbose_name="Transaction Type")
    amount_debited = models.DecimalField(blank=True, null=True, max_digits=15, decimal_places=2, verbose_name="Debit")
    last_transaction = models.DecimalField(blank=True, null=True, max_digits=15, decimal_places=2)
    amount_credited = models.DecimalField(blank=True, null=True, max_digits=15, decimal_places=2, verbose_name="Credit")
    current_balance = models.DecimalField(blank=True, null=True, max_digits=15, decimal_places=2)
    amount_credited = models.DecimalField(blank=True, null=True, max_digits=15, decimal_places=2, verbose_name="Credit")
    referral = models.DecimalField(blank=True, null=True, max_digits=15, decimal_places=2)
    first = models.DecimalField(blank=True, null=True, max_digits=15, decimal_places=2)
    point = models.DecimalField(blank=True, null=True, max_digits=15, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        try:
            return str(self.user.username) + " | " + str(self.user.first_name) + " " + str(self.user.last_name)
        except:
            return str(self.id)

    class Meta:
        ordering = ('-created',)

class Request(models.Model):
    user = models.ForeignKey('users.Person', null=True, on_delete=models.SET_NULL)
    amount_requested = models.CharField(max_length=50, null=True, verbose_name="Amount Transferred")
    payment_date = models.DateField(null=True, verbose_name="Payment Date")
    payment_evidence = models.ImageField(upload_to='credit_req/%Y/%m/%d', null=True, verbose_name="Upload Payment Evidence")
    waiver_code = models.CharField(max_length=10, null=True, blank=True, verbose_name="Waiver Code")
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('-created',)

class Subscription(models.Model):
    user = models.ForeignKey('users.Person', null=True, blank=True, on_delete=models.SET_NULL)
    request_Id = models.ForeignKey(Request, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    subscription_ends = models.DateField(null=True)

    def __str__(self):
        return str(self.request_Id)

    class Meta:
        ordering = ('-created',)
