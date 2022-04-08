import urllib.request
from datetime import datetime
from anticipate.models import AntiOrder
from orders.models import OrderStatus
from products.models import Category, Product, Cylinder, Owing
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomRegisterForm, CustomRegisterForm2, RequestForm, CustomRegisterFormQwikCust, CustomRegisterFormQwikAdmin, CustomRegisterFormQwikVendor, CustomRegisterFormQwikPartner, AdminCreditForm, OutletForm
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from .filters import WalletFilter, WalletFilter2, PeopleFilter, OutletFilter
from .models import Person, Wallet, Outlet
from orders.models import OrderItem
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
#from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db.models import Sum

from django.db.models.functions import ExtractMonth, ExtractYear, TruncMonth
from django.db.models import Count

#from django.template.loader import render_to_string

def create(request):
    if request.method == "POST":
        form = CustomRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration was successful!")
            return redirect('first_login')
        else:
            messages.error(request, "Please review and correct form input fields")
            #return redirect('account')
    else:
        form = CustomRegisterForm()
    return render(request, 'users/account.html', {'form': form})

def createFR(request, ref):
    if request.method == "POST":
        form = CustomRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False).referrer = ref
            form.save()
            messages.success(request, "Registration was successful!")
            return redirect('first_login')
        else:
            messages.error(request, "Please review and correct form input fields")
            #return redirect('account')
    else:
        form = CustomRegisterForm()
    return render(request, 'users/account.html', {'form': form})

# @login_required
# def editProfileAdminFirst(request, **kwargs):
#     if request.method == "POST":
#         form = CustomRegisterFormAdmin(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Your profile has been modified successfully")
#             return redirect('profile_admin_first')
#         else:
#             messages.error(request, "Error: Please review form input fields below")
#     else:
#         form = CustomRegisterFormAdmin(instance=request.user)
#     return render(request, 'users/profile_admin.html', {'form': form})
#
# @login_required
# def editProfileStaffFirst(request, **kwargs):
#     if request.method == "POST":
#         form = CustomRegisterFormStaff(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Your profile has been modified successfully")
#             return redirect('profile_staff_first')
#         else:
#             messages.error(request, "Error: Please review form input fields below")
#     else:
#         form = CustomRegisterFormStaff(instance=request.user)
#     return render(request, 'users/profile_staff.html', {'form': form})

@login_required
def editQwikCust(request, **kwargs):
    if request.method == "POST":
        form = CustomRegisterFormQwikCust(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been modified successfully")
            return redirect('qwikcust_profile')
        else:
            messages.error(request, "Error: Please review form input fields below")
    else:
        form = CustomRegisterFormQwikCust(instance=request.user)
    return render(request, 'users/qwikcust_profile.html', {'form': form})

@login_required
@permission_required('users.view_admin')
def editQwikAdmin(request, **kwargs):
    if request.method == "POST":
        form = CustomRegisterFormQwikAdmin(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been modified successfully")
            return redirect('qwikadmin_profile')
        else:
            messages.error(request, "Error: Please review form input fields below")
    else:
        form = CustomRegisterFormQwikAdmin(instance=request.user)
    return render(request, 'users/qwikadmin_profile.html', {'form': form})

@login_required
@permission_required('users.view_vendor')
def editQwikVendor(request, **kwargs):
    if request.method == "POST":
        form = CustomRegisterFormQwikVendor(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been modified successfully")
            return redirect('qwikvendor_profile')
        else:
            messages.error(request, "Error: Please review form input fields below")
    else:
        form = CustomRegisterFormQwikVendor(instance=request.user)
    return render(request, 'users/qwikvendor_profile.html', {'form': form})

@login_required
@permission_required('users.view_partner')
def editQwikPartner(request, **kwargs):
    if request.method == "POST":
        form = CustomRegisterFormQwikPartner(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been modified successfully")
            return redirect('qwikpartner_profile')
        else:
            messages.error(request, "Error: Please review form input fields below")
    else:
        form = CustomRegisterFormQwikPartner(instance=request.user)
    return render(request, 'users/qwikpartner_profile.html', {'form': form})

@login_required
def changePasswordQwikCust(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            user = request.user
            name = user.first_name
            email = user.email
            # send_mail(
            #     'Password Changed!',
            #     'Dear ' + str(name) + ', your password has just been changed. If this activity was not carried out by you, please reply to this email',
            #     'yustaoab@gmail.com',
            #     [email],
            #     fail_silently=False,
            #     html_message = render_to_string('users/change_password_email.html', {'name': str(name)})
            # )
            messages.success(request, "Your password has been changed successfully")
            return redirect('qwikcust_board')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'users/qwikcust_change_password.html', {'form': form})

@login_required
@permission_required('users.view_admin')
def changePasswordQwikAdmin(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            user = request.user
            name = user.first_name
            email = user.email
            # send_mail(
            #     'Password Changed!',
            #     'Dear ' + str(name) + ', your password has just been changed. If this activity was not carried out by you, please reply to this email',
            #     'yustaoab@gmail.com',
            #     [email],
            #     fail_silently=False,
            #     html_message = render_to_string('users/change_password_email.html', {'name': str(name)})
            # )
            messages.success(request, "Your password has been changed successfully")
            return redirect('qwikadmin_board')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'users/qwikadmin_change_password.html', {'form': form})

@login_required
@permission_required('users.view_admin')
def changePasswordQwikVendor(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            user = request.user
            name = user.first_name
            email = user.email
            # send_mail(
            #     'Password Changed!',
            #     'Dear ' + str(name) + ', your password has just been changed. If this activity was not carried out by you, please reply to this email',
            #     'yustaoab@gmail.com',
            #     [email],
            #     fail_silently=False,
            #     html_message = render_to_string('users/change_password_email.html', {'name': str(name)})
            # )
            messages.success(request, "Your password has been changed successfully")
            return redirect('qwikvendor_board')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'users/qwikvendor_change_password.html', {'form': form})

@login_required
@permission_required('users.view_admin')
def changePasswordQwikPartner(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            user = request.user
            name = user.first_name
            email = user.email
            # send_mail(
            #     'Password Changed!',
            #     'Dear ' + str(name) + ', your password has just been changed. If this activity was not carried out by you, please reply to this email',
            #     'yustaoab@gmail.com',
            #     [email],
            #     fail_silently=False,
            #     html_message = render_to_string('users/change_password_email.html', {'name': str(name)})
            # )
            messages.success(request, "Your password has been changed successfully")
            return redirect('qwikpartner_board')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'users/qwikpartner_change_password.html', {'form': form})

def showFirstLogin(request):
    try:
        wallet = Wallet.objects.filter(user=request.user)[0]
        current_balance = wallet.current_balance
    except:
        current_balance = 0.00
    try:
        first = Wallet.objects.get(user=request.user, transaction_type="QwikFirst")
    except:
        first = None
    try:
        referral = Wallet.objects.filter(user=request.user).aggregate(Sum('referral'))['referral__sum']
        referrals = round(referral,2)
    except:
        referrals = 0.00
    try:
        point = Wallet.objects.filter(user=request.user).aggregate(Sum('point'))['point__sum']
        points = round(point,2)
    except:
        points = 0.00

    username = str(request.user.username)

    try:
        referrers = Person.objects.filter(referrer=username).count()
    except:
        referrers = 0

    # category = None
    # categories = Category.objects.all()
    # products = Product.objects.filter(available=True)
    #products = Product.objects.filter(status__in=["At Ketu product (filled)","At Oshodi product (filled)"])
    # products = Product.objects.filter(Q(status="At Ketu product (filled)") | Q(status="At Oshodi product (filled)"))

    # today = datetime.today()
    # my_today = today.strftime('%d, %b %Y')

    return render(request, 'users/qwikcust_board.html', {'current_balance':current_balance,
                                                      'first':first,
                                                      'referrals': referrals,
                                                      'points': points,
                                                      'referrers': referrers})

@login_required
def showQwikCustBoard(request):
    try:
        wallet = Wallet.objects.filter(user=request.user)[0]
        current_balance = wallet.current_balance
    except:
        current_balance = 0.00
    try:
        first = Wallet.objects.get(user=request.user, transaction_type="QwikFirst")
    except:
        first = None
    try:
        referral = Wallet.objects.filter(user=request.user).aggregate(Sum('referral'))['referral__sum']
        referrals = round(referral,2)
    except:
        referrals = 0.00
    try:
        point = Wallet.objects.filter(user=request.user).aggregate(Sum('point'))['point__sum']
        points = round(point,2)
    except:
        points = 0.00

    username = str(request.user.username)

    try:
        referrers = Person.objects.filter(referrer=username).count()
    except:
        referrers = 0

    # order_items = OrderItem.objects.filter(order__user=request.user).order_by('created')

    order_items = OrderItem.objects.filter(order__user=request.user).order_by('created')




    # month = OrderItem.objects.values(month=ExtractMonth('created'),year=ExtractMonth('created')).filter(year=2022,month=1).count()

    #month = OrderItem.objects.filter(created__month='1').count()

    created_list = [""]
    quantity_list = [0]
    price_list = [0]
    point_list = [0]

    for each in order_items:
        created_list.append(each.created.strftime('%d, %b %Y'))
        quantity_list.append(each.quantity)
        price_list.append(str(each.get_cost()))

    return render(request, 'users/qwikcust_board.html', {'current_balance':current_balance,
                                                      'first':first,
                                                      'referrals': referrals,
                                                      'points': points,
                                                      'referrers': referrers,
                                                      'created_list': created_list,
                                                      'quantity_list': quantity_list,
                                                      'price_list': price_list})

@login_required
def showQwikCustWallets(request):
    context = {}
    filtered_wallets = WalletFilter(
        request.GET,
        queryset = Wallet.objects.filter(user=request.user)
    )
    context['filtered_wallets'] = filtered_wallets
    paginated_filtered_wallets = Paginator(filtered_wallets.qs, 10)
    page_number = request.GET.get('page')
    wallets_page_obj = paginated_filtered_wallets.get_page(page_number)
    context['wallets_page_obj'] = wallets_page_obj
    total_wallets = filtered_wallets.qs.count()
    context['total_wallets'] = total_wallets

    try:
        wallet = Wallet.objects.filter(user=request.user)[0]
        current_balance = wallet.current_balance
        context['current_balance'] = current_balance
    except:
        current_balance = 0.00
        context['current_balance'] = current_balance

    try:
        credit = Wallet.objects.filter(user=request.user).aggregate(Sum('amount_credited'))['amount_credited__sum']
        credits = round(credit,2)
    except:
        credits = 0
    try:
        referral = Wallet.objects.filter(user=request.user).aggregate(Sum('referral'))['referral__sum']
        referrals = round(referral,2)
    except:
        referrals = 0
    try:
        first = Wallet.objects.filter(user=request.user).aggregate(Sum('first'))['first__sum']
        firsts = round(first,2)
    except:
        firsts = 0
    try:
        point = Wallet.objects.filter(user=request.user).aggregate(Sum('point'))['point__sum']
        points = round(point,2)
    except:
        points = 0

    all = credits + referrals + firsts + points
    context['all'] = all
    try:
        debit = Wallet.objects.filter(user=request.user).aggregate(Sum('amount_debited'))['amount_debited__sum']
        debits = round(debit,2)
        context['debits'] = debits
    except:
        debits = 0.00
        context['debits'] = debits

    form = RequestForm()
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES, None)
        if form.is_valid():
            form.save(commit=False).user = request.user
            form.save()
            messages.success(request, "Your request has been sent successfully.")
            return redirect('qwikcust_wallets')
        else:
            messages.error(request, "Please review form input fields below")
    context['form'] = form

    return render(request, 'users/qwikcust_wallets.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminWallets(request):
    context = {}
    filtered_wallets = WalletFilter2(
        request.GET,
        queryset = Wallet.objects.all()
    )
    context['filtered_wallets'] = filtered_wallets
    paginated_filtered_wallets = Paginator(filtered_wallets.qs, 10)
    page_number = request.GET.get('page')
    wallets_page_obj = paginated_filtered_wallets.get_page(page_number)
    context['wallets_page_obj'] = wallets_page_obj
    total_wallets = filtered_wallets.qs.count()
    context['total_wallets'] = total_wallets

    try:
        debit = Wallet.objects.all().aggregate(Sum('amount_debited'))['amount_debited__sum']
        debits = round(debit,2)
        context['debits'] = debits
    except:
        debit = 0
        debits = 0
        context['debits'] = debits
    try:
        credit = Wallet.objects.all().aggregate(Sum('amount_credited'))['amount_credited__sum']
        credits = round(credit,2)
        context['credits'] = credits
    except:
        credit = 0
        credits = 0
        context['credits'] = credits
    try:
        referral = Wallet.objects.all().aggregate(Sum('referral'))['referral__sum']
        referrals = round(referral,2)
        context['referrals'] = referrals
    except:
        referral = 0
        referrals = 0
        context['referrals'] = referrals
    try:
        first = Wallet.objects.all().aggregate(Sum('first'))['first__sum']
        firsts = round(first,2)
        context['firsts'] = firsts
    except:
        first = 0
        firsts = 0
        context['firsts'] = firsts
    try:
        point = Wallet.objects.all().aggregate(Sum('point'))['point__sum']
        points = round(point,2)
        context['points'] = points
    except:
        point = 0
        points = 0
        context['points'] = points

    all = debit + credit + referral + first + point

    try:
        perc_debit = round((debit/all)*100,1)
        context['perc_debit'] = perc_debit
    except:
        perc_debit = 0
        context['perc_debit'] = perc_debit
    try:
        perc_credit = round((credit/all)*100,1)
        context['perc_credit'] = perc_credit
    except:
        perc_credit = 0
        context['perc_credit'] = perc_credit
    try:
        perc_referral = round((referral/all)*100,1)
        context['perc_referral'] = perc_referral
    except:
        perc_referral = 0
        context['perc_referral'] = perc_referral
    try:
        perc_first = round((first/all)*100,1)
        context['perc_first'] = perc_first
    except:
        perc_first = 0
        context['perc_first'] = perc_first
    try:
        perc_point = round((point/all)*100,1)
        context['perc_point'] = perc_point
    except:
        perc_point = 0
        context['perc_point'] = perc_point

    perc_d = round(perc_debit/100,2)
    context['perc_d'] = perc_d
    perc_c = round(perc_credit/100,2)
    context['perc_c'] = perc_c
    perc_r = round(perc_referral/100,2)
    context['perc_r'] = perc_r
    perc_f = round(perc_first/100,2)
    context['perc_f'] = perc_f
    perc_p = round(perc_point/100,2)
    context['perc_p'] = perc_p

    return render(request, 'users/qwikadmin_wallets.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminBoard(request):
    people = Person.objects.all().count()
    qwikcustomers = Person.objects.filter(type="QwikCustomer").count()
    qwikvendors = Person.objects.filter(type="QwikVendor").count()
    qwikpartners = Person.objects.filter(type="QwikPartner").count()
    qwikadmins = Person.objects.filter(type="QwikA--").count()

    perc_cust = round((qwikcustomers/people)*100,1)
    perc_vend = round((qwikvendors/people)*100,1)
    perc_part = round((qwikpartners/people)*100,1)
    perc_adm = round((qwikadmins/people)*100,1)

    cust = round(perc_cust/100,2)
    vend = round(perc_vend/100,2)
    part = round(perc_part/100,2)
    adm = round(perc_adm/100,2)

    return render(request, 'users/qwikadmin_board.html', {'qwikcustomers':qwikcustomers,
                                                          'perc_cust':perc_cust,
                                                          'qwikvendors':qwikvendors,
                                                          'perc_vend':perc_vend,
                                                          'qwikpartners':qwikpartners,
                                                          'perc_part':perc_part,
                                                          'qwikadmins':qwikadmins,
                                                          'perc_adm':perc_adm,
                                                          'cust':cust,
                                                          'vend':vend,
                                                          'part':part,
                                                          'adm':adm})

@login_required
@permission_required('users.view_admin')
def showQwikAdminPeople(request):
    context = {}
    filtered_people = PeopleFilter(
        request.GET,
        queryset = Person.objects.all()
    )
    context['filtered_people'] = filtered_people
    paginated_filtered_people = Paginator(filtered_people.qs, 10)
    page_number = request.GET.get('page')
    people_page_obj = paginated_filtered_people.get_page(page_number)
    context['people_page_obj'] = people_page_obj
    total_people = filtered_people.qs.count()
    context['total_people'] = total_people

    owings = Owing.objects.all()


    people = Person.objects.all().count()
    qwikcustomers = Person.objects.filter(type="QwikCustomer").count()
    qwikvendors = Person.objects.filter(type="QwikVendor").count()
    qwikpartners = Person.objects.filter(type="QwikPartner").count()
    qwikadmins = Person.objects.filter(type="QwikA--").count()

    perc_cust = round((qwikcustomers/people)*100,1)
    perc_vend = round((qwikvendors/people)*100,1)
    perc_part = round((qwikpartners/people)*100,1)
    perc_adm = round((qwikadmins/people)*100,1)

    cust = round(perc_cust/100,2)
    vend = round(perc_vend/100,2)
    part = round(perc_part/100,2)
    adm = round(perc_adm/100,2)

    context['qwikcustomers'] = qwikcustomers
    context['qwikvendors'] = qwikvendors
    context['qwikpartners'] = qwikpartners
    context['qwikadmins'] = qwikadmins

    context['perc_cust'] = perc_cust
    context['perc_vend'] = perc_vend
    context['perc_part'] = perc_part
    context['perc_adm'] = perc_adm

    context['cust'] = cust
    context['vend'] = vend
    context['part'] = part
    context['adm'] = adm

    return render(request, 'users/qwikadmin_people.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminOutlets(request):
    context = {}
    filtered_outlets = OutletFilter(
        request.GET,
        queryset = Outlet.objects.all()
    )
    context['filtered_outlets'] = filtered_outlets
    paginated_filtered_outlets = Paginator(filtered_outlets.qs, 10)
    page_number = request.GET.get('page')
    outlets_page_obj = paginated_filtered_outlets.get_page(page_number)
    context['outlets_page_obj'] = outlets_page_obj
    total_outlets = filtered_outlets.qs.count()
    context['total_outlets'] = total_outlets
    return render(request, 'users/qwikadmin_outlets.html', context=context)

@login_required
@permission_required('users.view_admin')
def deleteOutlet(request, id):
    outlet = Outlet.objects.get(id=id)
    obj = get_object_or_404(Outlet, id=id)
    if request.method =="POST":
        obj.delete()
        return redirect('qwikadmin_outlets')
    return render(request, 'users/qwikadmin_outlet_confirm_delete.html', {'outlet': outlet})

@login_required
@permission_required('users.view_admin')
def updateOutlet(request, id):
    outlet = Outlet.objects.get(id=id)
    form = OutletForm(instance=outlet)
    if request.method=='POST':
        form = OutletForm(request.POST, instance=outlet)
        if form.is_valid():
            form.save()
            messages.success(request, "The outlet has been modified successfully")
            return redirect('qwikadmin_outlets')
    return render(request, 'users/qwikadmin_outlet_update.html', {'form': form, 'outlet': outlet})

@login_required
@permission_required('users.view_vendor')
def showQwikVendorBoard(request):
    cylinders = Product.objects.filter(outlet__manager=request.user).count()
    dispatched_empties = Product.objects.filter(outlet__manager=request.user, vendor_product_status="Dispatched Empty").count()
    received_empties = Product.objects.filter(outlet__manager=request.user, vendor_product_status="Received Empty").count()
    dispatched_filleds = Product.objects.filter(outlet__manager=request.user, vendor_product_status="Dispatched Filled").count()
    received_filleds = Product.objects.filter(outlet__manager=request.user, vendor_product_status="Received Filled").count()

    try:
        perc_dispatched_empties = round((dispatched_empties/cylinders)*100,1)
    except:
        perc_dispatched_empties = 0
    try:
        perc_received_empties = round((received_empties/cylinders)*100,1)
    except:
        perc_received_empties = 0
    try:
        perc_dispatched_filleds = round((dispatched_filleds/cylinders)*100,1)
    except:
        perc_dispatched_filleds = 0
    try:
        perc_received_filleds = round((received_filleds/cylinders)*100,1)
    except:
        perc_received_filleds = 0

    dispatched_empty = round(perc_dispatched_empties/100,2)
    received_empty = round(perc_received_empties/100,2)
    dispatched_filled = round(perc_dispatched_filleds/100,2)
    received_filled = round(perc_received_filleds/100,2)

    standards = Product.objects.filter(outlet__manager=request.user, category__mass="12.5KG").count()
    premiums = Product.objects.filter(outlet__manager=request.user, category__mass="25KG").count()
    maxes = Product.objects.filter(outlet__manager=request.user, category__mass="50KG").count()

    try:
        perc_standards = round((standards/cylinders)*100,1)
    except:
        perc_standards = 0
    try:
        perc_premiums = round((premiums/cylinders)*100,1)
    except:
        perc_premiums = 0
    try:
        perc_maxes = round((maxes/cylinders)*100,1)
    except:
        perc_maxes = 0

    standard = round(perc_standards/100,2)
    premium = round(perc_premiums/100,2)
    max = round(perc_maxes/100,2)

    return render(request, 'users/qwikvendor_board.html', {'dispatched_empties':dispatched_empties,
                                                            'received_empties':received_empties,
                                                            'dispatched_filleds':dispatched_filleds,
                                                            'received_filleds':received_filleds,
                                                            'perc_dispatched_empties':perc_dispatched_empties,
                                                            'perc_received_empties':perc_received_empties,
                                                            'perc_dispatched_filleds':perc_dispatched_filleds,
                                                            'perc_received_filleds':perc_received_filleds,
                                                            'dispatched_empty':dispatched_empty,
                                                            'received_empty':received_empty,
                                                            'dispatched_filled':dispatched_filled,
                                                            'received_filled':received_filled,
                                                            'standards':standards,
                                                            'premiums':premiums,
                                                            'maxes':maxes,
                                                            'perc_standards':standards,
                                                            'perc_premiums':premiums,
                                                            'perc_maxes':maxes,
                                                            'standard':standard,
                                                            'premium':premium,
                                                            'max':max,
                                                            })

@login_required
@permission_required('users.view_partner')
def showQwikPartnerBoard(request):

    return render(request, 'users/qwikpartner_board.html')

@login_required
@permission_required('users.view_admin')
def createUser(request):
    if request.method == "POST":
        form = CustomRegisterForm2(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration was successful!")
            return redirect('qwikadmin_account')
        else:
            messages.error(request, "Please review and correct form input fields")
            #return redirect('account')
    else:
        form = CustomRegisterForm2()
    return render(request, 'users/qwikadmin_account.html', {'form': form})

@login_required
def loginTo(request):
    if request.user.type == "QwikCustomer":
        return HttpResponseRedirect(reverse('qwikcust_board'))
    elif request.user.type == "QwikA--":
        return HttpResponseRedirect(reverse('qwikadmin_board'))
    elif request.user.type == "QwikVendor":
        return HttpResponseRedirect(reverse('qwikvendor_board'))
    elif request.user.type == "QwikPartner":
        return HttpResponseRedirect(reverse('qwikpartner_board'))

@login_required
@permission_required('users.view_admin')
def creditWallet(request):
    form = AdminCreditForm()
    if request.method == 'POST':
        form = AdminCreditForm(request.POST or None)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('user')
            wallet_0 = Wallet.objects.filter(user=name)[0]
            try:
                wallet_1 = Wallet.objects.filter(user=name)[1]
                wallet_0.current_balance = wallet_0.amount_credited + wallet_1.current_balance
                wallet_0.last_tran = wallet_0.amount_credited
                wallet_0.transaction_type = "Credit"
                email = wallet_0.user.email
                name2 = wallet_0.user.first_name
                wallet_0.save()
                # send_mail(
                #     'Wallet Credit Confirmed',
                #     'Dear ' + str(name2) + ', Your wallet balance has been topped up',
                #     'admin@buildqwik.ng',
    			# 	[email, 'payment@buildqwik.ng'],
                #     fail_silently=False,
                #     html_message = render_to_string('users/credit_wallet_email.html', {'name': str(name2)})
                # )
                messages.success(request, str(name2) + "'s wallet balance has been topped up and email notification sent to him")
                return redirect('wallet_credit')
            except:
                wallet_0.current_balance = wallet_0.amount_credited
                wallet_0.last_tran = wallet_0.amount_credited
                wallet_0.transaction_type = "Credit"
                email = wallet_0.user.email
                name2 = wallet_0.user.first_name
                wallet_0.save()
                # send_mail(
                #     'Wallet Credit Confirmed',
                #     'Dear ' + str(name2) + ', Your wallet balance has been topped up',
                #     'admin@buildqwik.ng',
    			# 	[email],
                #     fail_silently=False,
                #     html_message = render_to_string('users/credit_wallet_email.html', {'name': str(name2)})
                # )
                messages.success(request, str(name2) + "'s wallet balance has been topped up and email notification sent to him")
                return redirect('wallet_credit')
    return render(request, 'users/qwikadmin_credit_form.html', {'form': form})

@login_required
@permission_required('users.view_admin')
def deletePerson(request, id):
    person = Person.objects.get(id=id)
    obj = get_object_or_404(Person, id=id)
    if request.method =="POST":
        obj.delete()
        return redirect('qwikadmin_people')
    return render(request, 'users/qwikadmin_person_confirm_delete.html', {'person': person})

@login_required
@permission_required('users.view_admin')
def updatePerson(request, id):
    person = Person.objects.get(id=id)
    form = CustomRegisterFormQwikAdmin(instance=person)
    if request.method=='POST':
        form = CustomRegisterFormQwikAdmin(request.POST, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, "The person has been modified successfully")
            return redirect('qwikadmin_people')
    return render(request, 'users/qwikadmin_person_update.html', {'form': form, 'person': person})

@login_required
@permission_required('users.view_admin')
def addOutlet(request):
    form = OutletForm()
    if request.method == 'POST':
        form = OutletForm(request.POST, request.FILES, None)
        if form.is_valid():
            form.save()
            messages.success(request, "The outlet has been added successfully")
            return redirect('qwikadmin_outlets')
        else:
            messages.error(request, "Please review form input fields below")
    return render(request, 'users/qwikadmin_outlet.html', {'form': form})
