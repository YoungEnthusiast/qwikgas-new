from django.contrib import admin
from .models import Person, Wallet, Lg, State, Outlet, Request
from .forms import CustomRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class PersonAdmin(UserAdmin):
    list_display = ['created', 'username', 'first_name', 'last_name', 'type', 'outlet', 'referrer', 'is_staff', 'is_superuser']
    list_display_links = ['username', 'first_name']
    search_fields = ['username', 'email', 'phone_number']
    list_filter = ['is_staff', 'is_superuser', 'type']
    list_editable = ['is_staff', 'is_superuser']
    list_per_page = 10

    add_form = CustomRegisterForm
    fieldsets = (
            *UserAdmin.fieldsets,
            (
                "Custom Fields",
                {
                    'fields': ('phone_number', 'gender', 'type', 'photograph', 'holding', 'address', 'state', 'lg', 'city', 'outlet', 'about_me', 'referrer')
                }
            )
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'gender', 'phone_number', 'type', 'photograph', 'address', 'state', 'lg', 'city', 'outlet', 'about_me', 'referrer')}
        ),
    )
admin.site.register(Person, PersonAdmin)

class WalletAdmin(admin.ModelAdmin):
    list_display = ['created', 'user', 'transaction_type', 'amount_debited', 'amount_credited', 'referral', 'first', 'current_balance']
    search_fields = ['user__username', 'amount_debited', 'amount_credited', 'current']
    list_filter = ['amount_debited', 'amount_credited']
    list_display_links = ['user']
    list_per_page = 10

admin.site.register(Wallet, WalletAdmin)

class LgAdmin(admin.ModelAdmin):
    list_display = ['created', 'lg']
    # search_fields = ['user__username', 'amount_debited', 'amount_credited', 'current']
    # list_filter = ['amount_debited', 'amount_credited']
    list_display_links = ['lg']
    list_per_page = 10

admin.site.register(Lg, LgAdmin)

class StateAdmin(admin.ModelAdmin):
    list_display = ['created', 'state']
    # search_fields = ['user__username', 'amount_debited', 'amount_credited', 'current']
    # list_filter = ['amount_debited', 'amount_credited']
    list_display_links = ['state']
    list_per_page = 10

admin.site.register(State, StateAdmin)

class OutletAdmin(admin.ModelAdmin):
    # list_display = ['created', 'outlet']
    list_display = ['outlet']
    # search_fields = ['user__username', 'amount_debited', 'amount_credited', 'current']
    # list_filter = ['amount_debited', 'amount_credited']
    list_display_links = ['outlet']
    list_per_page = 10

admin.site.register(Outlet, OutletAdmin)

class RequestAdmin(admin.ModelAdmin):
    # list_display = ['created', 'outlet']
    # list_display = ['outlet']
    # # search_fields = ['user__username', 'amount_debited', 'amount_credited', 'current']
    # # list_filter = ['amount_debited', 'amount_credited']
    # list_display_links = ['outlet']
    list_per_page = 10

admin.site.register(Request, RequestAdmin)
