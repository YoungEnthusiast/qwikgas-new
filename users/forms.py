from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import Person, Wallet, Outlet, Request
from django.core.exceptions import ValidationError
import datetime
from django.forms.widgets import NumberInput
from django.forms.widgets import TextInput

class CustomRegisterForm(UserCreationForm):
    GENDER_CHOICES = [
		('Male','Male'),
		('Female', 'Female')
	]
    TYPE_CHOICES = [
        ('QwikCustomer', 'QwikCustomer'),
		('QwikVendor', 'QwikVendor'),
        ('QwikPartner', 'QwikPartner'),
        ('QwikA', 'QwikA'),
    ]
    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES, widget=forms.RadioSelect, required=False)
    dob = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), required=False, label="Date of Start of Business")
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(required=False)
    username = forms.CharField(max_length=20)
    # def clean_email(self):
    #    email = self.cleaned_data.get('email')
    #    if Person.objects.filter(email=email).exists():
    #        raise ValidationError("A user with the supplied email already exists")
    #    return email

    def clean_username(self):
       username = self.cleaned_data.get('username')
       if Person.objects.filter(username=username).exists():
           raise ValidationError("A user with the supplied username already exists")
       return username

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'username', 'dob', 'com_name', 'password1', 'password2', 'phone_number', 'address', 'referrer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        #self.fields['username'].label = 'Admission No (Username)'
        #self.fields['username'].help_text = "For staff, choose a username for logging in in subsequent times"
        self.fields['email'].help_text = "This field must be a valid email address"
        self.fields['password1'].help_text = ""
        self.fields['password2'].label = "Password Confirmation"
        self.fields['phone_number'].label = "Phone Number"

class CustomRegisterForm2(UserCreationForm):
    GENDER_CHOICES = [
		('Male','Male'),
		('Female', 'Female')
	]
    TYPE_CHOICES = [
        ('QwikCustomer', 'QwikCustomer'),
		('QwikVendor', 'QwikVendor'),
        ('QwikPartner', 'QwikPartner'),
        ('QwikA', 'QwikA'),
    ]
    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES, widget=forms.RadioSelect, required=False)
    dob = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), required=False, label="Date of Start of Business")
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(required=False)
    username = forms.CharField(max_length=20)
    # def clean_email(self):
    #    email = self.cleaned_data.get('email')
    #    if Person.objects.filter(email=email).exists():
    #        raise ValidationError("A user with the supplied email already exists")
    #    return email

    def clean_username(self):
       username = self.cleaned_data.get('username')
       if Person.objects.filter(username=username).exists():
           raise ValidationError("A user with the supplied username already exists")
       return username

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'gender', 'username', 'dob', 'com_name', 'password1', 'password2', 'photograph', 'phone_number', 'address', 'state', 'lg', 'city', 'type', 'about_me', 'referrer', 'outlet']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        #self.fields['username'].label = 'Admission No (Username)'
        #self.fields['username'].help_text = "For staff, choose a username for logging in in subsequent times"
        self.fields['email'].help_text = "This field must be a valid email address"
        self.fields['password2'].label = "Password Confirmation"
        self.fields['phone_number'].label = "Phone Number"

class CustomRegisterFormQwikCust(UserChangeForm):
    GENDER_CHOICES = [
		('Male','Male'),
		('Female', 'Female')
	]
    TYPE_CHOICES = [
        ('QwikCustomer', 'QwikCustomer'),
		('QwikVendor', 'QwikVendor'),
        ('QwikPartner', 'QwikPartner'),
        ('QwikA', 'QwikA'),
    ]
    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES, widget=forms.RadioSelect, required=False)
    dob = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), required=False, label="Date of Start of Business")
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(required=False)
    username = forms.CharField(max_length=20)
    # def clean_email(self):
    #    email = self.cleaned_data.get('email')
    #    if Person.objects.filter(email=email).exists():
    #        raise ValidationError("A user with the supplied email already exists")
    #    return email

    def clean_dob(self):
        try:
            dob = self.cleaned_data.get('dob')
            if dob > datetime.date.today():
                raise ValidationError("The selected date is invalid. Please re-select another")
            return dob
        except:
            pass


    def __init__(self, *args, **kwargs):
        super(CustomRegisterFormQwikCust, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['username'].required = False
            self.fields['username'].widget.attrs['disabled'] = 'disabled'
            self.fields['first_name'].required = False
            self.fields['first_name'].widget.attrs['disabled'] = 'disabled'
            self.fields['last_name'].required = False
            self.fields['last_name'].widget.attrs['disabled'] = 'disabled'
            self.fields['referrer'].required = False
            self.fields['referrer'].widget.attrs['disabled'] = 'disabled'
            self.fields['first_name'].label = 'First Name'
            self.fields['last_name'].label = 'Last Name'
            self.fields['email'].help_text = "This field must be a valid email address"
            self.fields['phone_number'].label = "Phone Number"


    def clean_username(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.username
        else:
            return self.cleaned_data.get('username', None)

    def clean_first_name(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.first_name
        else:
            return self.cleaned_data.get('first_name', None)

    def clean_last_name(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.last_name
        else:
            return self.cleaned_data.get('last_name', None)

    def clean_referrer(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.referrer
        else:
            return self.cleaned_data.get('referrer', None)

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'username', 'com_name', 'dob', 'phone_number', 'gender', 'state', 'city', 'lg', 'outlet', 'about_me', 'address', 'referrer', 'photograph']

class CustomRegisterFormQwikVendor(UserChangeForm):
    GENDER_CHOICES = [
		('Male','Male'),
		('Female', 'Female')
	]
    TYPE_CHOICES = [
        ('QwikCustomer', 'QwikCustomer'),
		('QwikVendor', 'QwikVendor'),
        ('QwikPartner', 'QwikPartner'),
        ('QwikA', 'QwikA'),
    ]
    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES, widget=forms.RadioSelect, required=False)
    dob = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), required=False, label="Date of Start of Business")
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(required=False)
    username = forms.CharField(max_length=20)
    # def clean_email(self):
    #    email = self.cleaned_data.get('email')
    #    if Person.objects.filter(email=email).exists():
    #        raise ValidationError("A user with the supplied email already exists")
    #    return email

    def clean_dob(self):
        try:
            dob = self.cleaned_data.get('dob')
            if dob > datetime.date.today():
                raise ValidationError("The selected date is invalid. Please re-select another")
            return dob
        except:
            pass

    def __init__(self, *args, **kwargs):
        super(CustomRegisterFormQwikVendor, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['username'].required = False
            self.fields['username'].widget.attrs['disabled'] = 'disabled'
            self.fields['first_name'].required = False
            self.fields['first_name'].widget.attrs['disabled'] = 'disabled'
            self.fields['last_name'].required = False
            self.fields['last_name'].widget.attrs['disabled'] = 'disabled'
            self.fields['referrer'].required = False
            self.fields['referrer'].widget.attrs['disabled'] = 'disabled'
            self.fields['first_name'].label = 'First Name'
            self.fields['last_name'].label = 'Last Name'
            self.fields['email'].help_text = "This field must be a valid email address"
            self.fields['phone_number'].label = "Phone Number"


    def clean_username(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.username
        else:
            return self.cleaned_data.get('username', None)

    def clean_first_name(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.first_name
        else:
            return self.cleaned_data.get('first_name', None)

    def clean_last_name(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.last_name
        else:
            return self.cleaned_data.get('last_name', None)

    def clean_referrer(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.referrer
        else:
            return self.cleaned_data.get('referrer', None)

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'username', 'phone_number', 'gender', 'dob', 'state', 'city', 'lg', 'outlet', 'about_me', 'address', 'referrer', 'photograph']

class CustomRegisterFormQwikPartner(UserChangeForm):
    GENDER_CHOICES = [
		('Male','Male'),
		('Female', 'Female')
	]
    TYPE_CHOICES = [
        ('QwikCustomer', 'QwikCustomer'),
		('QwikVendor', 'QwikVendor'),
        ('QwikPartner', 'QwikPartner'),
        ('QwikA', 'QwikA'),
    ]
    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES, widget=forms.RadioSelect, required=False)
    dob = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), required=False, label="Date of Start of Business")
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(required=False)
    username = forms.CharField(max_length=20)
    # def clean_email(self):
    #    email = self.cleaned_data.get('email')
    #    if Person.objects.filter(email=email).exists():
    #        raise ValidationError("A user with the supplied email already exists")
    #    return email

    def clean_dob(self):
        try:
            dob = self.cleaned_data.get('dob')
            if dob > datetime.date.today():
                raise ValidationError("The selected date is invalid. Please re-select another")
            return dob
        except:
            pass

    def __init__(self, *args, **kwargs):
        super(CustomRegisterFormQwikPartner, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['username'].required = False
            self.fields['username'].widget.attrs['disabled'] = 'disabled'
            self.fields['first_name'].required = False
            self.fields['first_name'].widget.attrs['disabled'] = 'disabled'
            self.fields['last_name'].required = False
            self.fields['last_name'].widget.attrs['disabled'] = 'disabled'
            self.fields['referrer'].required = False
            self.fields['referrer'].widget.attrs['disabled'] = 'disabled'
            self.fields['first_name'].label = 'First Name'
            self.fields['last_name'].label = 'Last Name'
            self.fields['email'].help_text = "This field must be a valid email address"
            self.fields['phone_number'].label = "Phone Number"


    def clean_username(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.username
        else:
            return self.cleaned_data.get('username', None)

    def clean_first_name(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.first_name
        else:
            return self.cleaned_data.get('first_name', None)

    def clean_last_name(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.last_name
        else:
            return self.cleaned_data.get('last_name', None)

    def clean_referrer(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.referrer
        else:
            return self.cleaned_data.get('referrer', None)

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'username', 'phone_number', 'dob', 'gender', 'state', 'city', 'lg', 'outlet', 'about_me', 'address', 'referrer', 'photograph']


class CustomRegisterFormQwikAdmin(UserChangeForm):
    GENDER_CHOICES = [
		('Male','Male'),
		('Female', 'Female')
	]
    TYPE_CHOICES = [
        ('QwikCustomer', 'QwikCustomer'),
		('QwikVendor', 'QwikVendor'),
        ('QwikPartner', 'QwikPartner'),
        ('QwikA', 'QwikA'),
    ]
    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES, widget=forms.RadioSelect, required=False)
    dob = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), required=False, label="Date of Start of Business")
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    username = forms.CharField(max_length=20)
    # def clean_email(self):
    #    email = self.cleaned_data.get('email')
    #    if Person.objects.filter(email=email).exists():
    #        raise ValidationError("A user with the supplied email already exists")
    #    return email

    def clean_dob(self):
        try:
            dob = self.cleaned_data.get('dob')
            if dob > datetime.date.today():
                raise ValidationError("The selected date is invalid. Please re-select another")
            return dob
        except:
            pass

    def __init__(self, *args, **kwargs):
        super(CustomRegisterFormQwikAdmin, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['first_name'].label = 'First Name'
            self.fields['last_name'].label = 'Last Name'
            self.fields['email'].help_text = "This field must be a valid email address"
            self.fields['phone_number'].label = "Phone Number"


    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'username', 'phone_number', 'dob', 'gender', 'state', 'city', 'lg', 'outlet', 'type', 'about_me', 'address', 'outlet', 'photograph']

class AdminCreditForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['user', 'amount_credited']

class OutletForm(forms.ModelForm):
    class Meta:
        model = Outlet
        fields = ['manager', 'partner', 'outlet', 'address', 'email']

class AuthForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email'}))
    password = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email'}))

    class Meta:
        model = Person
        fieldset = ['username', 'password']

class RequestForm(forms.ModelForm):
    payment_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), label="Payment Date", required=False)
    class Meta:
        model = Request
        fields = '__all__'
        exclude = ['user']
