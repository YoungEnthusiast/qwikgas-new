from django.db import models

class Contact(models.Model):
    STATUS_CHOICES = [
        ('Treated','Treated'),
        ('New', 'New'),
        ('Pending', 'Pending')
    ]
    name = models.CharField(max_length=40, blank=True, null=True, verbose_name="Full Name")
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField(max_length=500, null=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='New', null=True)

    class Meta:
        ordering = ('-date_submitted',)
        verbose_name = 'Contact us Message'
        verbose_name_plural = 'Contact us Messages'

    def __str__(self):
        return str(self.name)
