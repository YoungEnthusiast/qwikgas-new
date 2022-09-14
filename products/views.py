from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, Cylinder, Owing
from anticipate.models import AntiOrder
from orders.models import UserOrder, OrderStatus
from users.models import Wallet, Outlet, Person
from .forms import CategoryForm, ProductForm, ProductFormPartner, ProductFormAdmin, CylinderFormVendor, CylinderFormAdminUp, CylinderFormAdminUpDispatchedToPlant, CylinderFormAdminUpReturnedFilledToQwikLet, CylinderFormAdminUpDispatchedToQwikCustomer, CylinderFormAdminUpDeliveredToQwikCustomerAnti, CylinderFormAdminUpDeliveredToQwikCustomerUser, CylinderFormPartner, CylinderFormVendorUp, CylinderFormPartnerUp, CylinderFormCustomerUp
# from orders.forms import VisitorOrderForm
from .filters import ProductFilter, ProductFilterAdmin, CategoryFilter, CylinderFilter, CylinderFilter2, CylinderFilter3
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
# from django.core.mail import send_mail
# from cart.forms import CartAddProductForm
# from django.template.loader import render_to_string
from datetime import datetime
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator
#from django.db.models import Q
from django.db.models import Sum

@login_required
def product_list(request, category_slug=None):
    try:
        wallet = Wallet.objects.filter(user=request.user)[0]
        current_balance = wallet.current_balance
    except:
        current_balance = 0
    try:
        first = Wallet.objects.get(user=request.user, transaction_type="QwikFirst")
    except:
        first = None
    try:
        referral = Wallet.objects.filter(user=request.user).aggregate(Sum('referral'))['referral__sum']
        referrals = round(referral,2)
    except:
        referrals = 0
    try:
        point = Wallet.objects.filter(user=request.user).aggregate(Sum('point'))['point__sum']
        points = round(point,2)
    except:
        points = 0

    username = str(request.user.username)

    try:
        referrers = Person.objects.filter(referrer=username).count()
    except:
        referrers = 0

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    #products = Product.objects.filter(status__in=["At Ketu product (filled)","At Oshodi product (filled)"])
    # products = Product.objects.filter(Q(status="At Ketu product (filled)") | Q(status="At Oshodi product (filled)"))

    today = datetime.today()
    my_today = today.strftime('%d, %b %Y')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'users/qwikcust_products.html', {'current_balance':current_balance,
                                                      'category': category,
                                                      'categories': categories,
                                                      'products': products,
                                                      'my_today': my_today,
                                                      'first':first,
                                                      'referrals': referrals,
                                                      'points': points,
                                                      'referrers': referrers})
@login_required
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'products/qwikcust_product_detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})

@login_required
def product_detail2(request, id):
    product = get_object_or_404(Product, id=id)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'products/qwikcust_product_detail2.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})

@login_required
@permission_required('users.view_vendor')
def showQwikVendorProducts(request):
    context = {}
    filtered_products = ProductFilter(
        request.GET,
        queryset = Product.objects.all()
    )
    context['filtered_products'] = filtered_products
    paginated_filtered_products = Paginator(filtered_products.qs, 10)
    page_number = request.GET.get('page')
    products_page_obj = paginated_filtered_products.get_page(page_number)
    context['products_page_obj'] = products_page_obj
    total_products = filtered_products.qs.count()
    context['total_products'] = total_products
    return render(request, 'products/qwikvendor_products.html', context=context)

@login_required
@permission_required('users.view_partner')
def showQwikPartnerCylindersReceivedEmpty(request):
    try:
        outlet_1 = Outlet.objects.filter(partner=request.user)[0]
    except:
        pass
    outlet_2 = outlet_1.outlet
    cylinders0 = Cylinder.objects.filter(outlet=outlet_2).count()
    cylinders_1 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1

    cylinders = cylinders0 + cylinders1 + cylinders2

    received_empty_from_qwikcustomers = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", outlet=outlet_2).count()
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True, outlet=outlet_2).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    dispatched_filled_to_qwikcustomers = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()

    delivered_to_qwikcustomers0 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1

    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()

    try:
        perc_received_empty_from_qwikcustomers = round((received_empty_from_qwikcustomers/cylinders)*100,1)
    except:
        perc_received_empty_from_qwikcustomers = 0
    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_dispatched_filled_to_qwikcustomers = round((dispatched_filled_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_dispatched_filled_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    received_empty_from_qwikcustomer = round(perc_received_empty_from_qwikcustomers/100,2)
    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    dispatched_filled_to_qwikcustomer = round(perc_dispatched_filled_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", outlet=outlet_2)
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['received_empty_from_qwikcustomers'] = received_empty_from_qwikcustomers
    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['dispatched_filled_to_qwikcustomers'] = dispatched_filled_to_qwikcustomers
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_received_empty_from_qwikcustomers'] = perc_received_empty_from_qwikcustomers
    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_dispatched_filled_to_qwikcustomers'] = perc_dispatched_filled_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['received_empty_from_qwikcustomer'] = received_empty_from_qwikcustomer
    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['dispatched_filled_to_qwikcustomer'] = dispatched_filled_to_qwikcustomer
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    form = CylinderFormPartner()
    if request.method == 'POST':
        form = CylinderFormPartner(request.POST, request.FILES, None)
        if form.is_valid():
            cylinder = form.cleaned_data.get('cylinder')
            customer = form.cleaned_data.get('customer')
            try:
                product = Product.objects.filter(product_Id=cylinder)[0]
                category = product.category.type
                outlet = product.outlet.outlet
            except:
                outlet = "None"
                category = "None"
            form.save(commit=False).partner_product_status = "Received Empty from QwikCustomer"
            form.save(commit=False).category = category
            form.save(commit=False).outlet = outlet
            form.save()

            try:
                reg = Product.objects.get(product_Id=cylinder)
                reg.partner_product_status = "Received Empty from QwikCustomer"
                reg.save()
            except:
                pass

            owings = Owing.objects.filter(customer=customer)
            for each in owings:
                each.cylinder = each.cylinder.replace(cylinder, "")
                each.save()

            owings = Owing.objects.filter(customer=customer)
            reg = Person.objects.get(username=customer.username)
            reg.holding = ""
            reg.save()
            reg1 = Person.objects.get(username=customer.username)
            for each in owings:
                reg1.holding = reg1.holding + "" + each.cylinder
                reg1.save()

            owings_2 = Owing.objects.filter(customer=customer)
            for each in owings_2:
                if each.cylinder == "":
                    each.delete()

            messages.success(request, "The cylinder stage has been added successfully")
            return redirect('products:qwikpartner_cylinders_received_empty')
        else:
            messages.error(request, "Please review form input fields below")
    context['form'] = form
    return render(request, 'products/qwikpartner_cylinders_received_empty.html', context=context)

@login_required
@permission_required('users.view_vendor')
def showQwikVendorCylindersDispatchedToPlant(request):
    try:
        outlet_1 = Outlet.objects.filter(manager=request.user)[0]
    except:
        pass
    outlet_2 = outlet_1.outlet
    cylinders0 = Cylinder.objects.filter(outlet=outlet_2).count()
    cylinders_1 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1

    cylinders = cylinders0 + cylinders1 + cylinders2
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True, outlet=outlet_2).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    released_filled_to_qwikpartners = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()

    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_released_filled_to_qwikpartners = round((released_filled_to_qwikpartners/cylinders)*100,1)
    except:
        perc_released_filled_to_qwikpartners = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    released_filled_to_qwikpartner = round(perc_released_filled_to_qwikpartners/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", outlet=outlet_2)
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['released_filled_to_qwikpartners'] = released_filled_to_qwikpartners
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_released_filled_to_qwikpartners'] = perc_released_filled_to_qwikpartners
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['released_filled_to_qwikpartner'] = released_filled_to_qwikpartner
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    form = CylinderFormVendor()
    if request.method == 'POST':
        form = CylinderFormVendor(request.POST, request.FILES, None)
        if form.is_valid():
            cylinder = form.cleaned_data.get('cylinder')
            try:
                product = Product.objects.filter(product_Id=cylinder)[0]
                category = product.category.type
                outlet = product.outlet.outlet
            except:
                category = "None"
                outlet = "None"
            form.save(commit=False).vendor_product_status = "Dispatched to Plant"
            form.save(commit=False).category = category
            form.save(commit=False).outlet = outlet
            form.save()

            try:
                reg = Product.objects.get(product_Id=cylinder)
                reg.vendor_product_status = "Dispatched to Plant"
                reg.save()
            except:
                pass

            messages.success(request, "The cylinder stage has been added successfully")
            return redirect('products:qwikvendor_cylinders_dispatched_to_plant')
        else:
            messages.error(request, "Please review form input fields below")
    context['form'] = form
    return render(request, 'products/qwikvendor_cylinders_dispatched_to_plant.html', context=context)

@login_required
@permission_required('users.view_vendor')
def showQwikVendorCylindersReleasedFilledToQwikPartner(request):
    try:
        outlet_1 = Outlet.objects.filter(manager=request.user)[0]
    except:
        pass
    outlet_2 = outlet_1.outlet
    cylinders0 = Cylinder.objects.filter(outlet=outlet_2).count()
    cylinders_1 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True, outlet=outlet_2).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    released_filled_to_qwikpartners = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()

    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_released_filled_to_qwikpartners = round((released_filled_to_qwikpartners/cylinders)*100,1)
    except:
        perc_released_filled_to_qwikpartners = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    released_filled_to_qwikpartner = round(perc_released_filled_to_qwikpartners/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", outlet=outlet_2)
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['released_filled_to_qwikpartners'] = released_filled_to_qwikpartners
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_released_filled_to_qwikpartners'] = perc_released_filled_to_qwikpartners
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['released_filled_to_qwikpartner'] = released_filled_to_qwikpartner
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    form = CylinderFormVendor()
    if request.method == 'POST':
        form = CylinderFormVendor(request.POST, request.FILES, None)
        if form.is_valid():
            cylinder = form.cleaned_data.get('cylinder')
            try:
                product = Product.objects.filter(product_Id=cylinder)[0]
                category = product.category.type
                outlet = product.outlet.outlet
            except:
                category = "None"
                outlet = "None"
            form.save(commit=False).vendor_product_status = "Released Filled to QwikPartner"
            form.save(commit=False).category = category
            form.save(commit=False).outlet = outlet
            form.save()

            try:
                reg = Product.objects.get(product_Id=cylinder)
                reg.vendor_product_status = "Released Filled to QwikPartner"
                reg.partner_product_status = "Unselected"
                reg.save()
            except:
                pass
            messages.success(request, "The cylinder stage has been added successfully")
            return redirect('products:qwikvendor_cylinders_released_filled_to_qwikpartner')
        else:
            messages.error(request, "Please review form input fields below")
    context['form'] = form
    return render(request, 'products/qwikvendor_cylinders_released_filled_to_qwikpartner.html', context=context)

@login_required
@permission_required('users.view_partner')
def showQwikPartnerCylindersDispatchedFilledToQwikCustomer(request):
    try:
        outlet_1 = Outlet.objects.filter(partner=request.user)[0]
    except:
        pass
    outlet_2 = outlet_1.outlet
    cylinders0 = Cylinder.objects.filter(outlet=outlet_2).count()
    cylinders_1 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2

    received_empty_from_qwikcustomers = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", outlet=outlet_2).count()
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True, outlet=outlet_2).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    dispatched_filled_to_qwikcustomers = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()

    try:
        perc_received_empty_from_qwikcustomers = round((received_empty_from_qwikcustomers/cylinders)*100,1)
    except:
        perc_received_empty_from_qwikcustomers = 0
    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_dispatched_filled_to_qwikcustomers = round((dispatched_filled_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_dispatched_filled_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    received_empty_from_qwikcustomer = round(perc_received_empty_from_qwikcustomers/100,2)
    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    dispatched_filled_to_qwikcustomer = round(perc_dispatched_filled_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", outlet=outlet_2)
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['received_empty_from_qwikcustomers'] = received_empty_from_qwikcustomers
    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['dispatched_filled_to_qwikcustomers'] = dispatched_filled_to_qwikcustomers
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_received_empty_from_qwikcustomers'] = perc_received_empty_from_qwikcustomers
    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_dispatched_filled_to_qwikcustomers'] = perc_dispatched_filled_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['received_empty_from_qwikcustomer'] = received_empty_from_qwikcustomer
    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['dispatched_filled_to_qwikcustomer'] = dispatched_filled_to_qwikcustomer
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    return render(request, 'products/qwikpartner_cylinders_dispatched_filled_to_qwikcustomer.html', context=context)

@login_required
@permission_required('users.view_partner')
def showQwikPartnerCylindersDispatchedToPlant(request):
    try:
        outlet_1 = Outlet.objects.filter(partner=request.user)[0]
    except:
        pass
    outlet_2 = outlet_1.outlet
    cylinders0 = Cylinder.objects.filter(outlet=outlet_2).count()
    cylinders_1 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2

    received_empty_from_qwikcustomers = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", outlet=outlet_2).count()
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True, outlet=outlet_2).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    dispatched_filled_to_qwikcustomers = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()

    try:
        perc_received_empty_from_qwikcustomers = round((received_empty_from_qwikcustomers/cylinders)*100,1)
    except:
        perc_received_empty_from_qwikcustomers = 0
    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_dispatched_filled_to_qwikcustomers = round((dispatched_filled_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_dispatched_filled_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    received_empty_from_qwikcustomer = round(perc_received_empty_from_qwikcustomers/100,2)
    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    dispatched_filled_to_qwikcustomer = round(perc_dispatched_filled_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", outlet=outlet_2)
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['received_empty_from_qwikcustomers'] = received_empty_from_qwikcustomers
    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['dispatched_filled_to_qwikcustomers'] = dispatched_filled_to_qwikcustomers
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_received_empty_from_qwikcustomers'] = perc_received_empty_from_qwikcustomers
    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_dispatched_filled_to_qwikcustomers'] = perc_dispatched_filled_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['received_empty_from_qwikcustomer'] = received_empty_from_qwikcustomer
    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['dispatched_filled_to_qwikcustomer'] = dispatched_filled_to_qwikcustomer
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    return render(request, 'products/qwikpartner_cylinders_dispatched_to_plant.html', context=context)

@login_required
@permission_required('users.view_partner')
def showQwikPartnerCylindersDeliveredFilledToQwikLet(request):
    try:
        outlet_1 = Outlet.objects.filter(partner=request.user)[0]
    except:
        pass
    outlet_2 = outlet_1.outlet
    cylinders0 = Cylinder.objects.filter(outlet=outlet_2).count()
    cylinders_1 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2

    received_empty_from_qwikcustomers = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", outlet=outlet_2).count()
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True, outlet=outlet_2).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    dispatched_filled_to_qwikcustomers = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()

    try:
        perc_received_empty_from_qwikcustomers = round((received_empty_from_qwikcustomers/cylinders)*100,1)
    except:
        perc_received_empty_from_qwikcustomers = 0
    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_dispatched_filled_to_qwikcustomers = round((dispatched_filled_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_dispatched_filled_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    received_empty_from_qwikcustomer = round(perc_received_empty_from_qwikcustomers/100,2)
    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    dispatched_filled_to_qwikcustomer = round(perc_dispatched_filled_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2)
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['received_empty_from_qwikcustomers'] = received_empty_from_qwikcustomers
    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['dispatched_filled_to_qwikcustomers'] = dispatched_filled_to_qwikcustomers
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_received_empty_from_qwikcustomers'] = perc_received_empty_from_qwikcustomers
    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_dispatched_filled_to_qwikcustomers'] = perc_dispatched_filled_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['received_empty_from_qwikcustomer'] = received_empty_from_qwikcustomer
    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['dispatched_filled_to_qwikcustomer'] = dispatched_filled_to_qwikcustomer
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    return render(request, 'products/qwikpartner_cylinders_delivered_filled_to_qwiklet.html', context=context)

@login_required
@permission_required('users.view_vendor')
def showQwikVendorCylindersDeliveredFilledToQwikLet(request):
    try:
        outlet_1 = Outlet.objects.filter(manager=request.user)[0]
    except:
        pass
    outlet_2 = outlet_1.outlet
    cylinders0 = Cylinder.objects.filter(outlet=outlet_2).count()
    cylinders_1 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True, outlet=outlet_2).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    released_filled_to_qwikpartners = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()

    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_released_filled_to_qwikpartners = round((released_filled_to_qwikpartners/cylinders)*100,1)
    except:
        perc_released_filled_to_qwikpartners = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    released_filled_to_qwikpartner = round(perc_released_filled_to_qwikpartners/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2)
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['released_filled_to_qwikpartners'] = released_filled_to_qwikpartners
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_released_filled_to_qwikpartners'] = perc_released_filled_to_qwikpartners
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['released_filled_to_qwikpartner'] = released_filled_to_qwikpartner
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    return render(request, 'products/qwikvendor_cylinders_delivered_filled_to_qwiklet.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminCylindersDeliveredFilledToQwikLet(request):
    cylinders0 = Cylinder.objects.all().count()
    cylinders_1 = AntiOrder.objects.all()
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2
    received_empty_from_qwikcustomers = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer").count()
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True).count()
    dispatched_filled_to_qwikcustomers = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.all()
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True).count()

    try:
        perc_received_empty_from_qwikcustomers = round((received_empty_from_qwikcustomers/cylinders)*100,1)
    except:
        perc_received_empty_from_qwikcustomers = 0
    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_dispatched_filled_to_qwikcustomers = round((dispatched_filled_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_dispatched_filled_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    received_empty_from_qwikcustomer = round(perc_received_empty_from_qwikcustomers/100,2)
    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    dispatched_filled_to_qwikcustomer = round(perc_dispatched_filled_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter3(
        request.GET,
        queryset = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True)
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['received_empty_from_qwikcustomers'] = received_empty_from_qwikcustomers
    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['dispatched_filled_to_qwikcustomers'] = dispatched_filled_to_qwikcustomers
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_received_empty_from_qwikcustomers'] = perc_received_empty_from_qwikcustomers
    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_dispatched_filled_to_qwikcustomers'] = perc_dispatched_filled_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['received_empty_from_qwikcustomer'] = received_empty_from_qwikcustomer
    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['dispatched_filled_to_qwikcustomer'] = dispatched_filled_to_qwikcustomer
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    return render(request, 'products/qwikadmin_cylinders_delivered_filled_to_qwiklet.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminCylindersDispatchedToPlant(request):
    cylinders0 = Cylinder.objects.all().count()
    cylinders_1 = AntiOrder.objects.all()
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2
    received_empty_from_qwikcustomers = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer").count()
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True).count()
    dispatched_filled_to_qwikcustomers = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.all()
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True).count()

    try:
        perc_received_empty_from_qwikcustomers = round((received_empty_from_qwikcustomers/cylinders)*100,1)
    except:
        perc_received_empty_from_qwikcustomers = 0
    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_dispatched_filled_to_qwikcustomers = round((dispatched_filled_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_dispatched_filled_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    received_empty_from_qwikcustomer = round(perc_received_empty_from_qwikcustomers/100,2)
    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    dispatched_filled_to_qwikcustomer = round(perc_dispatched_filled_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter3(
        request.GET,
        queryset = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant")
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['received_empty_from_qwikcustomers'] = received_empty_from_qwikcustomers
    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['dispatched_filled_to_qwikcustomers'] = dispatched_filled_to_qwikcustomers
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_received_empty_from_qwikcustomers'] = perc_received_empty_from_qwikcustomers
    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_dispatched_filled_to_qwikcustomers'] = perc_dispatched_filled_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['received_empty_from_qwikcustomer'] = received_empty_from_qwikcustomer
    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['dispatched_filled_to_qwikcustomer'] = dispatched_filled_to_qwikcustomer
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    return render(request, 'products/qwikadmin_cylinders_dispatched_to_plant.html', context=context)

@login_required
@permission_required('users.view_partner')
def showQwikPartnerCylindersReturnedEmpty(request):
    try:
        outlet_1 = Outlet.objects.filter(partner=request.user)[0]
    except:
        pass
    outlet_2 = outlet_1.outlet
    cylinders0 = Cylinder.objects.filter(outlet=outlet_2).count()
    cylinders_1 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2

    received_empty_from_qwikcustomers = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", outlet=outlet_2).count()
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True, outlet=outlet_2).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    dispatched_filled_to_qwikcustomers = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()

    try:
        perc_received_empty_from_qwikcustomers = round((received_empty_from_qwikcustomers/cylinders)*100,1)
    except:
        perc_received_empty_from_qwikcustomers = 0
    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_dispatched_filled_to_qwikcustomers = round((dispatched_filled_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_dispatched_filled_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    received_empty_from_qwikcustomer = round(perc_received_empty_from_qwikcustomers/100,2)
    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    dispatched_filled_to_qwikcustomer = round(perc_dispatched_filled_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", outlet=outlet_2)
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['received_empty_from_qwikcustomers'] = received_empty_from_qwikcustomers
    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['dispatched_filled_to_qwikcustomers'] = dispatched_filled_to_qwikcustomers
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_received_empty_from_qwikcustomers'] = perc_received_empty_from_qwikcustomers
    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_dispatched_filled_to_qwikcustomers'] = perc_dispatched_filled_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['received_empty_from_qwikcustomer'] = received_empty_from_qwikcustomer
    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['dispatched_filled_to_qwikcustomer'] = dispatched_filled_to_qwikcustomer
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    return render(request, 'products/qwikpartner_cylinders_returned_empty.html', context=context)

@login_required
@permission_required('users.view_partner')
def showQwikPartnerCylindersReturnedFilledToQwikLet(request):
    try:
        outlet_1 = Outlet.objects.filter(partner=request.user)[0]
    except:
        pass
    outlet_2 = outlet_1.outlet
    cylinders0 = Cylinder.objects.filter(outlet=outlet_2).count()
    cylinders_1 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2

    received_empty_from_qwikcustomers = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", outlet=outlet_2).count()
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True, outlet=outlet_2).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    dispatched_filled_to_qwikcustomers = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()

    try:
        perc_received_empty_from_qwikcustomers = round((received_empty_from_qwikcustomers/cylinders)*100,1)
    except:
        perc_received_empty_from_qwikcustomers = 0
    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_dispatched_filled_to_qwikcustomers = round((dispatched_filled_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_dispatched_filled_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    received_empty_from_qwikcustomer = round(perc_received_empty_from_qwikcustomers/100,2)
    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    dispatched_filled_to_qwikcustomer = round(perc_dispatched_filled_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2))
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer"))
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['received_empty_from_qwikcustomers'] = received_empty_from_qwikcustomers
    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['dispatched_filled_to_qwikcustomers'] = dispatched_filled_to_qwikcustomers
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_received_empty_from_qwikcustomers'] = perc_received_empty_from_qwikcustomers
    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_dispatched_filled_to_qwikcustomers'] = perc_dispatched_filled_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['received_empty_from_qwikcustomer'] = received_empty_from_qwikcustomer
    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['dispatched_filled_to_qwikcustomer'] = dispatched_filled_to_qwikcustomer
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    return render(request, 'products/qwikpartner_cylinders_returned_filled_to_qwiklet.html', context=context)

@login_required
@permission_required('users.view_vendor')
def showQwikVendorCylindersReturnedFilledToQwikLet(request):
    try:
        outlet_1 = Outlet.objects.filter(manager=request.user)[0]
    except:
        pass
    outlet_2 = outlet_1.outlet
    cylinders0 = Cylinder.objects.filter(outlet=outlet_2).count()
    cylinders_1 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True, outlet=outlet_2).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    released_filled_to_qwikpartners = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()

    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_released_filled_to_qwikpartners = round((released_filled_to_qwikpartners/cylinders)*100,1)
    except:
        perc_released_filled_to_qwikpartners = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    released_filled_to_qwikpartner = round(perc_released_filled_to_qwikpartners/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2))
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer"))
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['released_filled_to_qwikpartners'] = released_filled_to_qwikpartners
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_released_filled_to_qwikpartners'] = perc_released_filled_to_qwikpartners
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['released_filled_to_qwikpartner'] = released_filled_to_qwikpartner
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    return render(request, 'products/qwikvendor_cylinders_returned_filled_to_qwiklet.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminCylindersReturnedFilledToQwikLet(request):
    cylinders0 = Cylinder.objects.all().count()
    cylinders_1 = AntiOrder.objects.all()
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2
    received_empty_from_qwikcustomers = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer").count()
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True).count()
    dispatched_filled_to_qwikcustomers = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True).count()

    delivered_to_qwikcustomers0 = AntiOrder.objects.all()
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1

    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True).count()

    try:
        perc_received_empty_from_qwikcustomers = round((received_empty_from_qwikcustomers/cylinders)*100,1)
    except:
        perc_received_empty_from_qwikcustomers = 0
    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_dispatched_filled_to_qwikcustomers = round((dispatched_filled_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_dispatched_filled_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    received_empty_from_qwikcustomer = round(perc_received_empty_from_qwikcustomers/100,2)
    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    dispatched_filled_to_qwikcustomer = round(perc_dispatched_filled_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter3(
        request.GET,
        queryset = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True))
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer"))
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['received_empty_from_qwikcustomers'] = received_empty_from_qwikcustomers
    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['dispatched_filled_to_qwikcustomers'] = dispatched_filled_to_qwikcustomers
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_received_empty_from_qwikcustomers'] = perc_received_empty_from_qwikcustomers
    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_dispatched_filled_to_qwikcustomers'] = perc_dispatched_filled_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['received_empty_from_qwikcustomer'] = received_empty_from_qwikcustomer
    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['dispatched_filled_to_qwikcustomer'] = dispatched_filled_to_qwikcustomer
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    return render(request, 'products/qwikadmin_cylinders_returned_filled_to_qwiklet.html', context=context)

@login_required
@permission_required('users.view_vendor')
def showQwikVendorCylindersDeliveredToQwikCustomerAnti(request):
    try:
        outlet_1 = Outlet.objects.filter(manager=request.user)[0]
    except:
        pass
    outlet_2 = outlet_1.outlet
    cylinders0 = Cylinder.objects.filter(outlet=outlet_2).count()
    cylinders_1 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True, outlet=outlet_2).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    released_filled_to_qwikpartners = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()

    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_released_filled_to_qwikpartners = round((released_filled_to_qwikpartners/cylinders)*100,1)
    except:
        perc_released_filled_to_qwikpartners = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    released_filled_to_qwikpartner = round(perc_released_filled_to_qwikpartners/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = AntiOrder.objects.filter(outlet__outlet=outlet_2)
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['released_filled_to_qwikpartners'] = released_filled_to_qwikpartners
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_released_filled_to_qwikpartners'] = perc_released_filled_to_qwikpartners
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['released_filled_to_qwikpartner'] = released_filled_to_qwikpartner
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    return render(request, 'products/qwikvendor_cylinders_delivered_to_qwikcustomer_anti.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminCylindersDeliveredToQwikCustomerAnti(request):
    cylinders0 = Cylinder.objects.all().count()
    cylinders_1 = AntiOrder.objects.all()
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2
    received_empty_from_qwikcustomers = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer").count()
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True).count()
    dispatched_filled_to_qwikcustomers = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.all()
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True).count()

    try:
        perc_received_empty_from_qwikcustomers = round((received_empty_from_qwikcustomers/cylinders)*100,1)
    except:
        perc_received_empty_from_qwikcustomers = 0
    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_dispatched_filled_to_qwikcustomers = round((dispatched_filled_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_dispatched_filled_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    received_empty_from_qwikcustomer = round(perc_received_empty_from_qwikcustomers/100,2)
    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    dispatched_filled_to_qwikcustomer = round(perc_dispatched_filled_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = AntiOrder.objects.all()
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['received_empty_from_qwikcustomers'] = received_empty_from_qwikcustomers
    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['dispatched_filled_to_qwikcustomers'] = dispatched_filled_to_qwikcustomers
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_received_empty_from_qwikcustomers'] = perc_received_empty_from_qwikcustomers
    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_dispatched_filled_to_qwikcustomers'] = perc_dispatched_filled_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['received_empty_from_qwikcustomer'] = received_empty_from_qwikcustomer
    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['dispatched_filled_to_qwikcustomer'] = dispatched_filled_to_qwikcustomer
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    return render(request, 'products/qwikadmin_cylinders_delivered_to_qwikcustomer_anti.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminCylindersDeliveredToQwikCustomerUser(request):
    cylinders0 = Cylinder.objects.all().count()
    cylinders_1 = AntiOrder.objects.all()
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2
    received_empty_from_qwikcustomers = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer").count()
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True).count()
    dispatched_filled_to_qwikcustomers = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.all()
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True).count()

    try:
        perc_received_empty_from_qwikcustomers = round((received_empty_from_qwikcustomers/cylinders)*100,1)
    except:
        perc_received_empty_from_qwikcustomers = 0
    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_dispatched_filled_to_qwikcustomers = round((dispatched_filled_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_dispatched_filled_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    received_empty_from_qwikcustomer = round(perc_received_empty_from_qwikcustomers/100,2)
    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    dispatched_filled_to_qwikcustomer = round(perc_dispatched_filled_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = OrderStatus.objects.filter(order_status="Delivered")
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['received_empty_from_qwikcustomers'] = received_empty_from_qwikcustomers
    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['dispatched_filled_to_qwikcustomers'] = dispatched_filled_to_qwikcustomers
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_received_empty_from_qwikcustomers'] = perc_received_empty_from_qwikcustomers
    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_dispatched_filled_to_qwikcustomers'] = perc_dispatched_filled_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['received_empty_from_qwikcustomer'] = received_empty_from_qwikcustomer
    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['dispatched_filled_to_qwikcustomer'] = dispatched_filled_to_qwikcustomer
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    return render(request, 'products/qwikadmin_cylinders_delivered_to_qwikcustomer_user.html', context=context)

@login_required
@permission_required('users.view_partner')
def showQwikPartnerCylindersDeliveredToQwikCustomerAnti(request):
    try:
        outlet_1 = Outlet.objects.filter(partner=request.user)[0]
    except:
        pass
    outlet_2 = outlet_1.outlet
    cylinders0 = Cylinder.objects.filter(outlet=outlet_2).count()
    cylinders_1 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2

    received_empty_from_qwikcustomers = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", outlet=outlet_2).count()
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True, outlet=outlet_2).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    dispatched_filled_to_qwikcustomers = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()

    try:
        perc_received_empty_from_qwikcustomers = round((received_empty_from_qwikcustomers/cylinders)*100,1)
    except:
        perc_received_empty_from_qwikcustomers = 0
    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_dispatched_filled_to_qwikcustomers = round((dispatched_filled_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_dispatched_filled_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    received_empty_from_qwikcustomer = round(perc_received_empty_from_qwikcustomers/100,2)
    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    dispatched_filled_to_qwikcustomer = round(perc_dispatched_filled_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = AntiOrder.objects.filter(outlet__outlet=outlet_2)
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['received_empty_from_qwikcustomers'] = received_empty_from_qwikcustomers
    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['dispatched_filled_to_qwikcustomers'] = dispatched_filled_to_qwikcustomers
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_received_empty_from_qwikcustomers'] = perc_received_empty_from_qwikcustomers
    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_dispatched_filled_to_qwikcustomers'] = perc_dispatched_filled_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['received_empty_from_qwikcustomer'] = received_empty_from_qwikcustomer
    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['dispatched_filled_to_qwikcustomer'] = dispatched_filled_to_qwikcustomer
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    return render(request, 'products/qwikpartner_cylinders_delivered_to_qwikcustomer_anti.html', context=context)

@login_required
@permission_required('users.view_partner')
def showQwikPartnerCylindersDeliveredToQwikCustomerUser(request):
    try:
        outlet_1 = Outlet.objects.filter(partner=request.user)[0]
    except:
        pass
    outlet_2 = outlet_1.outlet
    cylinders0 = Cylinder.objects.filter(outlet=outlet_2).count()
    cylinders_1 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2

    received_empty_from_qwikcustomers = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", outlet=outlet_2).count()
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True, outlet=outlet_2).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    dispatched_filled_to_qwikcustomers = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()

    try:
        perc_received_empty_from_qwikcustomers = round((received_empty_from_qwikcustomers/cylinders)*100,1)
    except:
        perc_received_empty_from_qwikcustomers = 0
    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_dispatched_filled_to_qwikcustomers = round((dispatched_filled_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_dispatched_filled_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    received_empty_from_qwikcustomer = round(perc_received_empty_from_qwikcustomers/100,2)
    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    dispatched_filled_to_qwikcustomer = round(perc_dispatched_filled_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['received_empty_from_qwikcustomers'] = received_empty_from_qwikcustomers
    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['dispatched_filled_to_qwikcustomers'] = dispatched_filled_to_qwikcustomers
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_received_empty_from_qwikcustomers'] = perc_received_empty_from_qwikcustomers
    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_dispatched_filled_to_qwikcustomers'] = perc_dispatched_filled_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['received_empty_from_qwikcustomer'] = received_empty_from_qwikcustomer
    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['dispatched_filled_to_qwikcustomer'] = dispatched_filled_to_qwikcustomer
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    return render(request, 'products/qwikpartner_cylinders_delivered_to_qwikcustomer_user.html', context=context)

@login_required
@permission_required('users.view_vendor')
def showQwikVendorCylindersDeliveredToQwikCustomerUser(request):
    try:
        outlet_1 = Outlet.objects.filter(manager=request.user)[0]
    except:
        pass
    outlet_2 = outlet_1.outlet
    cylinders0 = Cylinder.objects.filter(outlet=outlet_2).count()
    cylinders_1 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True, outlet=outlet_2).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    released_filled_to_qwikpartners = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()

    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_released_filled_to_qwikpartners = round((released_filled_to_qwikpartners/cylinders)*100,1)
    except:
        perc_released_filled_to_qwikpartners = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    released_filled_to_qwikpartner = round(perc_released_filled_to_qwikpartners/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['released_filled_to_qwikpartners'] = released_filled_to_qwikpartners
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_released_filled_to_qwikpartners'] = perc_released_filled_to_qwikpartners
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['released_filled_to_qwikpartner'] = released_filled_to_qwikpartner
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    return render(request, 'products/qwikvendor_cylinders_delivered_to_qwikcustomer_user.html', context=context)

@login_required
@permission_required('users.view_vendor')
def showQwikVendorCylindersReturnedEmpty(request):
    try:
        outlet_1 = Outlet.objects.filter(manager=request.user)[0]
    except:
        pass
    outlet_2 = outlet_1.outlet
    cylinders0 = Cylinder.objects.filter(outlet=outlet_2).count()
    cylinders_1 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True, outlet=outlet_2).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True, outlet=outlet_2).count()
    released_filled_to_qwikpartners = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.filter(outlet__outlet=outlet_2)
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order__order__outlet__outlet=outlet_2, order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True, outlet=outlet_2).count()

    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_released_filled_to_qwikpartners = round((released_filled_to_qwikpartners/cylinders)*100,1)
    except:
        perc_released_filled_to_qwikpartners = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    released_filled_to_qwikpartner = round(perc_released_filled_to_qwikpartners/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", outlet=outlet_2)
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['released_filled_to_qwikpartners'] = released_filled_to_qwikpartners
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_released_filled_to_qwikpartners'] = perc_released_filled_to_qwikpartners
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['released_filled_to_qwikpartner'] = released_filled_to_qwikpartner
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    return render(request, 'products/qwikvendor_cylinders_returned_empty.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminCylindersReceivedEmpty(request):
    cylinders0 = Cylinder.objects.all().count()

    cylinders_1 = AntiOrder.objects.all()
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2
    received_empty_from_qwikcustomers = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer").count()
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True).count()
    dispatched_filled_to_qwikcustomers = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.all()
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True).count()

    try:
        perc_received_empty_from_qwikcustomers = round((received_empty_from_qwikcustomers/cylinders)*100,1)
    except:
        perc_received_empty_from_qwikcustomers = 0
    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_dispatched_filled_to_qwikcustomers = round((dispatched_filled_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_dispatched_filled_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    received_empty_from_qwikcustomer = round(perc_received_empty_from_qwikcustomers/100,2)
    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    dispatched_filled_to_qwikcustomer = round(perc_dispatched_filled_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer")
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['received_empty_from_qwikcustomers'] = received_empty_from_qwikcustomers
    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['dispatched_filled_to_qwikcustomers'] = dispatched_filled_to_qwikcustomers
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_received_empty_from_qwikcustomers'] = perc_received_empty_from_qwikcustomers
    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_dispatched_filled_to_qwikcustomers'] = perc_dispatched_filled_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['received_empty_from_qwikcustomer'] = received_empty_from_qwikcustomer
    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['dispatched_filled_to_qwikcustomer'] = dispatched_filled_to_qwikcustomer
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    return render(request, 'products/qwikadmin_cylinders_received_empty.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminCylindersReturnedEmpty(request):
    cylinders0 = Cylinder.objects.all().count()
    cylinders_1 = AntiOrder.objects.all()
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2
    received_empty_from_qwikcustomers = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer").count()
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True).count()
    dispatched_filled_to_qwikcustomers = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.all()
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True).count()

    try:
        perc_received_empty_from_qwikcustomers = round((received_empty_from_qwikcustomers/cylinders)*100,1)
    except:
        perc_received_empty_from_qwikcustomers = 0
    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_dispatched_filled_to_qwikcustomers = round((dispatched_filled_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_dispatched_filled_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    received_empty_from_qwikcustomer = round(perc_received_empty_from_qwikcustomers/100,2)
    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    dispatched_filled_to_qwikcustomer = round(perc_dispatched_filled_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter2(
        request.GET,
        queryset = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer")
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['received_empty_from_qwikcustomers'] = received_empty_from_qwikcustomers
    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['dispatched_filled_to_qwikcustomers'] = dispatched_filled_to_qwikcustomers
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_received_empty_from_qwikcustomers'] = perc_received_empty_from_qwikcustomers
    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_dispatched_filled_to_qwikcustomers'] = perc_dispatched_filled_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['received_empty_from_qwikcustomer'] = received_empty_from_qwikcustomer
    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['dispatched_filled_to_qwikcustomer'] = dispatched_filled_to_qwikcustomer
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    return render(request, 'products/qwikadmin_cylinders_returned_empty.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminCylindersDispatchedFilledToQwikCustomer(request):
    cylinders0 = Cylinder.objects.all().count()
    cylinders_1 = AntiOrder.objects.all()
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2
    received_empty_from_qwikcustomers = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer").count()
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", vendor_confirm=True).count()
    dispatched_to_plants = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True).count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Dispatched to Plant", partner_confirm=True).count()
    dispatched_filled_to_qwikcustomers = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True).count()
    delivered_to_qwikcustomers0 = AntiOrder.objects.all()
    delivered_to_qwikcustomers = 0
    for each in delivered_to_qwikcustomers0:
        for each_2 in each.cylinder.all():
            delivered_to_qwikcustomers += 1

    delivered_to_qwikcustomers_users0 = OrderStatus.objects.filter(order_status="Delivered")
    delivered_to_qwikcustomers_users = 0
    for each1 in delivered_to_qwikcustomers_users0:
        for each_3 in each.cylinder.all():
            delivered_to_qwikcustomers_users += 1
    returned_filled_to_qwiklets = Cylinder.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_confirm=True).count()

    try:
        perc_received_empty_from_qwikcustomers = round((received_empty_from_qwikcustomers/cylinders)*100,1)
    except:
        perc_received_empty_from_qwikcustomers = 0
    try:
        perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwiklets = 0
    try:
        perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    except:
        perc_dispatched_to_plants = 0
    try:
        perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_delivered_filled_to_qwiklets = 0
    try:
        perc_dispatched_filled_to_qwikcustomers = round((dispatched_filled_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_dispatched_filled_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers = 0
    try:
        perc_delivered_to_qwikcustomers_users = round((delivered_to_qwikcustomers_users/cylinders)*100,1)
    except:
        perc_delivered_to_qwikcustomers_users = 0
    try:
        perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)
    except:
        perc_returned_filled_to_qwiklets = 0

    received_empty_from_qwikcustomer = round(perc_received_empty_from_qwikcustomers/100,2)
    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    dispatched_filled_to_qwikcustomer = round(perc_dispatched_filled_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer_user = round(perc_delivered_to_qwikcustomers_users/100,2)
    returned_filled_to_qwiklet = round(perc_returned_filled_to_qwiklets/100,2)

    context = {}
    filtered_cylinders = CylinderFilter3(
        request.GET,
        queryset = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer")
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['received_empty_from_qwikcustomers'] = received_empty_from_qwikcustomers
    context['returned_empty_to_qwiklets'] = returned_empty_to_qwiklets
    context['dispatched_to_plants'] = dispatched_to_plants
    context['delivered_filled_to_qwiklets'] = delivered_filled_to_qwiklets
    context['dispatched_filled_to_qwikcustomers'] = dispatched_filled_to_qwikcustomers
    context['delivered_to_qwikcustomers'] = delivered_to_qwikcustomers
    context['delivered_to_qwikcustomers_users'] = delivered_to_qwikcustomers_users
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_received_empty_from_qwikcustomers'] = perc_received_empty_from_qwikcustomers
    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_dispatched_filled_to_qwikcustomers'] = perc_dispatched_filled_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers_users'] = perc_delivered_to_qwikcustomers_users
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['received_empty_from_qwikcustomer'] = received_empty_from_qwikcustomer
    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['dispatched_filled_to_qwikcustomer'] = dispatched_filled_to_qwikcustomer
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['delivered_to_qwikcustomer_user'] = delivered_to_qwikcustomer_user
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet
    return render(request, 'products/qwikadmin_cylinders_dispatched_filled_to_qwikcustomer.html', context=context)

@login_required
@permission_required('users.view_admin')
def updateQwikAdminCylindersReceivedEmpty(request, id):
    cylinder = Cylinder.objects.get(id=id)
    form = CylinderFormAdminUp(instance=cylinder)
    if request.method=='POST':
        form = CylinderFormAdminUp(request.POST, instance=cylinder)
        if form.is_valid():

            cylinder = form.cleaned_data.get('cylinder')
            try:
                product = Product.objects.filter(product_Id=cylinder)[0]
                category = product.category.type
            except:
                category = "None"
            form.save(commit=False).category = category
            form.save(commit=False).who_2 = "QwikAdmin"
            form.save()

            messages.success(request, "The cylinder has been modified successfully")
            return redirect('products:qwikadmin_cylinders_received_empty')
    return render(request, 'products/form_qwikadmin_received_empty.html', {'form': form, 'cylinder': cylinder})

@login_required
@permission_required('users.view_admin')
def updateQwikAdminCylindersDispatchedToPlant(request, id):
    cylinder = Cylinder.objects.get(id=id)
    form = CylinderFormAdminUpDispatchedToPlant(instance=cylinder)
    if request.method=='POST':
        form = CylinderFormAdminUpDispatchedToPlant(request.POST, instance=cylinder)
        if form.is_valid():

            cylinder = form.cleaned_data.get('cylinder')
            try:
                product = Product.objects.filter(product_Id=cylinder)[0]
                category = product.category.type
            except:
                category = "None"
            form.save(commit=False).category = category
            form.save(commit=False).who3_2 = "QwikAdmin"
            form.save()

            messages.success(request, "The cylinder has been modified successfully")
            return redirect('products:qwikadmin_cylinders_dispatched_to_plant')
    return render(request, 'products/form_qwikadmin_cylinders_dispatched_to_plant.html', {'form': form, 'cylinder': cylinder})

@login_required
@permission_required('users.view_admin')
def updateQwikAdminCylindersReturnedFilledToQwikLet(request, id):
    cylinder = Cylinder.objects.get(id=id)
    form = CylinderFormAdminUpReturnedFilledToQwikLet(instance=cylinder)
    if request.method=='POST':
        form = CylinderFormAdminUpReturnedFilledToQwikLet(request.POST, instance=cylinder)
        if form.is_valid():

            cylinder = form.cleaned_data.get('cylinder')
            try:
                product = Product.objects.filter(product_Id=cylinder)[0]
                category = product.category.type
            except:
                category = "None"
            form.save(commit=False).category = category
            form.save(commit=False).who8_2 = "QwikAdmin"
            form.save()

            messages.success(request, "The cylinder has been modified successfully")
            return redirect('products:qwikadmin_cylinders_returned_filled_to_qwiklet')
    return render(request, 'products/form_qwikadmin_cylinders_returned_filled_to_qwiklet.html', {'form': form, 'cylinder': cylinder})


@login_required
@permission_required('users.view_admin')
def updateQwikAdminCylindersDispatchedFilledToQwikCustomer(request, id):
    cylinder = Cylinder.objects.get(id=id)
    form = CylinderFormAdminUpDispatchedToQwikCustomer(instance=cylinder)
    if request.method=='POST':
        form = CylinderFormAdminUpDispatchedToQwikCustomer(request.POST, instance=cylinder)
        if form.is_valid():
            cylinder = form.cleaned_data.get('cylinder')
            try:
                product = Product.objects.filter(product_Id=cylinder)[0]
                category = product.category.type
            except:
                category = "None"
            form.save(commit=False).category = category
            form.save(commit=False).who5_2 = "QwikAdmin"
            form.save()

            messages.success(request, "The cylinder has been modified successfully")
            return redirect('products:qwikadmin_cylinders_dispatched_filled_to_qwikcustomer')
    return render(request, 'products/form_qwikadmin_cylinders_dispatched_filled_to_qwikcustomer.html', {'form': form, 'cylinder': cylinder})

@login_required
@permission_required('users.view_admin')
def updateQwikAdminCylindersDeliveredToQwikCustomerAnti(request, id):
    cylinder = AntiOrder.objects.get(id=id)
    form = CylinderFormAdminUpDeliveredToQwikCustomerAnti(instance=cylinder)
    if request.method=='POST':
        form = CylinderFormAdminUpDeliveredToQwikCustomerAnti(request.POST, instance=cylinder)
        if form.is_valid():

            # cylinder = form.cleaned_data.get('cylinder')
            # try:
            #     product = Product.objects.filter(product_Id=cylinder)[0]
            #     category = product.category.type
            # except:
            #     category = "None"
            # form.save(commit=False).category = category
            form.save(commit=False).who6_2 = "QwikAdmin"
            form.save()

            messages.success(request, "The cylinder has been modified successfully")
            return redirect('products:qwikadmin_cylinders_delivered_to_qwikcustomer_anti')
    return render(request, 'products/form_qwikadmin_cylinders_delivered_to_qwikcustomer_anti.html', {'form': form, 'cylinder': cylinder})

@login_required
@permission_required('users.view_admin')
def updateQwikAdminCylindersDeliveredToQwikCustomerUser(request, id):
    cylinder = OrderStatus.objects.get(id=id)
    form = CylinderFormAdminUpDeliveredToQwikCustomerUser(instance=cylinder)
    if request.method=='POST':
        form = CylinderFormAdminUpDeliveredToQwikCustomerUser(request.POST, instance=cylinder)
        if form.is_valid():

            # cylinder = form.cleaned_data.get('cylinder')
            # try:
            #     product = Product.objects.filter(product_Id=cylinder)[0]
            #     category = product.category.type
            # except:
            #     category = "None"
            # form.save(commit=False).category = category
            form.save(commit=False).who7_2 = "QwikAdmin"
            form.save()

            messages.success(request, "The cylinder has been modified successfully")
            return redirect('products:qwikadmin_cylinders_delivered_to_qwikcustomer_user')
    return render(request, 'products/form_qwikadmin_cylinders_delivered_to_qwikcustomer_user.html', {'form': form, 'cylinder': cylinder})

@login_required
@permission_required('users.view_admin')
def updateQwikAdminCylindersReturnedEmpty(request, id):
    cylinder = Cylinder.objects.get(id=id)
    form = CylinderFormAdminUpReturnedEmpty(instance=cylinder)
    if request.method=='POST':
        form = CylinderFormAdminUpReturnedEmpty(request.POST, instance=cylinder)
        if form.is_valid():

            cylinder = form.cleaned_data.get('cylinder')
            try:
                product = Product.objects.filter(product_Id=cylinder)[0]
                category = product.category.type
            except:
                category = "None"
            form.save(commit=False).category = category
            form.save(commit=False).who2_2 = "QwikAdmin"
            form.save()

            messages.success(request, "The cylinder has been modified successfully")
            return redirect('products:qwikadmin_cylinders_returned_empty')
    return render(request, 'products/form_qwikadmin_returned_empty.html', {'form': form, 'cylinder': cylinder})

@login_required
def showQwikCustomerCylindersReturnedEmpty(request):
    cylinders0 = Cylinder.objects.filter(customer=request.user).count()
    cylinders_1 = AntiOrder.objects.filter(user=request.user)
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order__order__user=request.user, order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2
    returned_empty_to_qwikpartners = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", customer=request.user).count()
    received_filleds0 = AntiOrder.objects.filter(user=request.user)
    received_filleds = 0
    for each in received_filleds0:
        for each_2 in each.cylinder.all():
            received_filleds += 1

    received_filleds_users0 = OrderStatus.objects.filter(order__order__user=request.user, order_status="Delivered")
    received_filleds_users = 0
    for each1 in received_filleds_users0:
        for each_3 in each.cylinder.all():
            received_filleds_users += 1
    try:
        perc_returned_empty_to_qwikpartners = round((returned_empty_to_qwikpartners/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwikpartners = 0
    try:
        perc_received_filleds = round((received_filleds/cylinders)*100,1)
    except:
        perc_received_filleds = 0
    try:
        perc_received_filleds_users = round((received_filleds_users/cylinders)*100,1)
    except:
        perc_received_filleds_users = 0

    returned_empty_to_qwikpartner = round(perc_returned_empty_to_qwikpartners/100,2)
    received_filled = round(perc_received_filleds/100,2)
    received_filled_user = round(perc_received_filleds_users/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", customer=request.user)
        # queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user, partner_product_status="Received Empty from QwikCustomer")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['returned_empty_to_qwikpartners'] = returned_empty_to_qwikpartners
    context['received_filleds'] = received_filleds
    context['received_filleds_users'] = received_filleds_users

    context['perc_returned_empty_to_qwikpartners'] = perc_returned_empty_to_qwikpartners
    context['perc_received_filleds'] = perc_received_filleds
    context['perc_received_filleds_users'] = perc_received_filleds_users

    context['returned_empty_to_qwikpartner'] = returned_empty_to_qwikpartner
    context['returned_received_filled'] = received_filled
    context['returned_received_filled_user'] = received_filled_user

    return render(request, 'products/qwikcustomer_cylinders_returned_empty.html', context=context)

@login_required
def showQwikCustomerCylindersReceivedFilledAnti(request):
    cylinders0 = Cylinder.objects.filter(customer=request.user).count()
    cylinders_1 = AntiOrder.objects.filter(user=request.user)
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1

    cylinders_2 = OrderStatus.objects.filter(order__order__user=request.user, order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1

    cylinders = cylinders0 + cylinders1 + cylinders2
    returned_empty_to_qwikpartners = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", customer=request.user).count()
    received_filleds0 = AntiOrder.objects.filter(user=request.user)
    received_filleds = 0
    for each in received_filleds0:
        for each_2 in each.cylinder.all():
            received_filleds += 1

    received_filleds_users0 = OrderStatus.objects.filter(order__order__user=request.user, order_status="Delivered")
    received_filleds_users = 0
    for each1 in received_filleds_users0:
        for each_3 in each.cylinder.all():
            received_filleds_users += 1

    try:
        perc_returned_empty_to_qwikpartners = round((returned_empty_to_qwikpartners/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwikpartners = 0
    try:
        perc_received_filleds = round((received_filleds/cylinders)*100,1)
    except:
        perc_received_filleds = 0
    try:
        perc_received_filleds_users = round((received_filleds_users/cylinders)*100,1)
    except:
        perc_received_filleds_users = 0

    returned_empty_to_qwikpartner = round(perc_returned_empty_to_qwikpartners/100,2)
    received_filled = round(perc_received_filleds/100,2)
    received_filled_user = round(perc_received_filleds_users/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = AntiOrder.objects.filter(user=request.user)
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['returned_empty_to_qwikpartners'] = returned_empty_to_qwikpartners
    context['received_filleds'] = received_filleds
    context['received_filleds_users'] = received_filleds_users

    context['perc_returned_empty_to_qwikpartners'] = perc_returned_empty_to_qwikpartners
    context['perc_received_filleds'] = perc_received_filleds
    context['perc_received_filleds_users'] = perc_received_filleds_users

    context['returned_empty_to_qwikpartner'] = returned_empty_to_qwikpartner
    context['returned_received_filled'] = received_filled
    context['returned_received_filled_user'] = received_filled_user

    return render(request, 'products/qwikcustomer_cylinders_received_filled_anti.html', context=context)

@login_required
def showQwikCustomerCylindersReceivedFilledUser(request):
    cylinders0 = Cylinder.objects.filter(customer=request.user).count()
    cylinders_1 = AntiOrder.objects.filter(user=request.user)
    cylinders1 = 0
    for each_cylinders_1 in cylinders_1:
        for each_cylinders1 in each_cylinders_1.cylinder.all():
            cylinders1 += 1
    cylinders_2 = OrderStatus.objects.filter(order__order__user=request.user, order_status="Delivered")
    cylinders2 = 0
    for each_cylinders_2 in cylinders_2:
        for each_cylinders2 in each_cylinders_2.cylinder.all():
            cylinders2 += 1
    cylinders = cylinders0 + cylinders1 + cylinders2
    returned_empty_to_qwikpartners = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer", customer=request.user).count()
    received_filleds0 = AntiOrder.objects.filter(user=request.user)
    received_filleds = 0
    for each_received_filleds0 in received_filleds0:
        for each_received_filleds in each_received_filleds0.cylinder.all():
            received_filleds += 1

    received_filleds_users0 = OrderStatus.objects.filter(order__order__user=request.user, order_status="Delivered")
    received_filleds_users = 0
    for each_received_filleds_users0 in received_filleds_users0:
        for each_received_filleds_users in each_received_filleds_users0.cylinder.all():
            received_filleds_users += 1
    try:
        perc_returned_empty_to_qwikpartners = round((returned_empty_to_qwikpartners/cylinders)*100,1)
    except:
        perc_returned_empty_to_qwikpartners = 0
    try:
        perc_received_filleds = round((received_filleds/cylinders)*100,1)
    except:
        perc_received_filleds = 0
    try:
        perc_received_filleds_users = round((received_filleds_users/cylinders)*100,1)
    except:
        perc_received_filleds_users = 0

    returned_empty_to_qwikpartner = round(perc_returned_empty_to_qwikpartners/100,2)
    received_filled = round(perc_received_filleds/100,2)
    received_filled_user = round(perc_received_filleds_users/100,2)

    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = OrderStatus.objects.filter(order__order__user=request.user, order_status="Delivered")
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders

    context['returned_empty_to_qwikpartners'] = returned_empty_to_qwikpartners
    context['received_filleds'] = received_filleds
    context['received_filleds_users'] = received_filleds_users

    context['perc_returned_empty_to_qwikpartners'] = perc_returned_empty_to_qwikpartners
    context['perc_received_filleds'] = perc_received_filleds
    context['perc_received_filleds_users'] = perc_received_filleds_users

    context['returned_empty_to_qwikpartner'] = returned_empty_to_qwikpartner
    context['received_filled'] = received_filled
    context['received_filled_user'] = received_filled_user

    return render(request, 'products/qwikcustomer_cylinders_received_filled_user.html', context=context)

@login_required
@permission_required('users.view_admin')
def returnQwikAdminCylindersReturnedFilledToQwikLet(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.vendor_confirm = True
    cylinder.who8 = "Return Filled"
    cylinder.who8_2 = "QwikAdmin"
    cylinder.save()
    return redirect('products:qwikadmin_cylinders_returned_filled_to_qwiklet')

@login_required
@permission_required('users.view_admin')
def notReturnQwikAdminCylindersReturnedFilledToQwikLet(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.vendor_confirm = True
    cylinder.who8 = "Not Returned Filled"
    cylinder.who8_2 = "QwikAdmin"
    cylinder.save()
    return redirect('products:qwikadmin_cylinders_returned_filled_to_qwiklet')

@login_required
@permission_required('users.view_admin')
def acceptQwikAdminCylindersReturnedFilledToQwikLet(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.vendor_confirm = True
    cylinder.who8_1 = "Accepted"
    cylinder.who8_2 = "QwikAdmin"
    cylinder.save()
    return redirect('products:qwikadmin_cylinders_returned_filled_to_qwiklet')

@login_required
@permission_required('users.view_admin')
def declineQwikAdminCylindersReturnedFilledToQwikLet(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.vendor_confirm = True
    cylinder.who8_1 = "Declined"
    cylinder.who8_2 = "QwikAdmin"
    cylinder.save()
    return redirect('products:qwikadmin_cylinders_returned_filled_to_qwiklet')

@login_required
@permission_required('users.view_vendor')
def acceptQwikVendorCylindersReturnedFilledToQwikLet(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.vendor_confirm = True
    cylinder.who8_1 = "Accepted"
    cylinder.save()
    return redirect('products:qwikvendor_cylinders_returned_filled_to_qwiklet')

@login_required
@permission_required('users.view_vendor')
def declineQwikVendorCylindersReturnedFilledToQwikLet(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.vendor_confirm = True
    cylinder.who8_1 = "Declined"
    cylinder.save()
    return redirect('products:qwikvendor_cylinders_returned_filled_to_qwiklet')

@login_required
@permission_required('users.view_vendor')
def acceptQwikVendorCylindersReturnedEmpty(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.vendor_confirm = True
    cylinder.who2 = "Accepted"
    cylinder.save()
    return redirect('products:qwikvendor_cylinders_returned_empty')

@login_required
@permission_required('users.view_vendor')
def declineQwikVendorCylindersReturnedEmpty(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.vendor_confirm = False
    cylinder.who2 = "Declined"
    cylinder.save()
    return redirect('products:qwikvendor_cylinders_returned_empty')

@login_required
@permission_required('users.view_partner')
def acceptQwikPartnerCylindersDispatchedToPlant(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.partner_confirm = True
    cylinder.who3 = "Accepted"
    cylinder.save()
    return redirect('products:qwikpartner_cylinders_dispatched_to_plant')

@login_required
@permission_required('users.view_partner')
def returnQwikPartnerCylindersReturnedFilledToQwikLet(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.partner_confirm = True
    cylinder.who8 = "Returned Filled"
    cylinder.save()
    return redirect('products:qwikpartner_cylinders_returned_filled_to_qwiklet')

@login_required
@permission_required('users.view_partner')
def declineQwikPartnerCylindersDispatchedToPlant(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.partner_confirm = False
    cylinder.who3 = "Declined"
    cylinder.save()
    return redirect('products:qwikpartner_cylinders_dispatched_to_plant')

@login_required
@permission_required('users.view_partner')
def acceptQwikPartnerCylindersDispatchedFilledToQwikCustomer(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.partner_confirm = True
    cylinder.who5 = "Accepted"
    cylinder.save()
    return redirect('products:qwikpartner_cylinders_dispatched_filled_to_qwikcustomer')

@login_required
@permission_required('users.view_partner')
def declineQwikPartnerCylindersDispatchedFilledToQwikCustomer(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.partner_confirm = False
    cylinder.who5 = "Declined"
    cylinder.save()
    return redirect('products:qwikpartner_cylinders_dispatched_filled_to_qwikcustomer')

@login_required
@permission_required('users.view_admin')
def acceptQwikAdminCylindersDispatchedFilledToQwikCustomer(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.partner_confirm = True
    cylinder.who5 = "Accepted"
    cylinder.who5_2 = "QwikAdmin"
    cylinder.save()
    return redirect('products:qwikadmin_cylinders_dispatched_filled_to_qwikcustomer')

@login_required
@permission_required('users.view_admin')
def declineQwikAdminCylindersDispatchedFilledToQwikCustomer(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.partner_confirm = False
    cylinder.who5 = "Declined"
    cylinder.who5_2 = "QwikAdmin"
    cylinder.save()
    return redirect('products:qwikadmin_cylinders_dispatched_filled_to_qwikcustomer')

@login_required
@permission_required('users.view_vendor')
def acceptQwikVendorCylindersDeliveredFilledToQwikLet(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.vendor_confirm = True
    cylinder.who4 = "Accepted"
    cylinder.save()
    return redirect('products:qwikvendor_cylinders_delivered_filled_to_qwiklet')

@login_required
@permission_required('users.view_vendor')
def declineQwikVendorCylindersDeliveredFilledToQwikLet(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.vendor_confirm = False
    cylinder.who4 = "Declined"
    cylinder.save()
    return redirect('products:qwikvendor_cylinders_delivered_filled_to_qwiklet')

@login_required
@permission_required('users.view_admin')
def acceptQwikAdminCylindersDeliveredFilledToQwikLet(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.vendor_confirm = True
    cylinder.who4 = "Accepted"
    cylinder.who4_2 = "QwikAdmin"
    cylinder.save()
    return redirect('products:qwikadmin_cylinders_delivered_filled_to_qwiklet')

@login_required
@permission_required('users.view_admin')
def declineQwikAdminCylindersDeliveredFilledToQwikLet(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.vendor_confirm = False
    cylinder.who4 = "Declined"
    cylinder.who4_2 = "QwikAdmin"
    cylinder.save()
    return redirect('products:qwikadmin_cylinders_delivered_filled_to_qwiklet')

@login_required
@permission_required('users.view_admin')
def acceptQwikAdminCylindersDispatchedToPlant(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.partner_confirm = True
    cylinder.who3 = "Accepted"
    cylinder.who3_2 = "QwikAdmin"
    cylinder.save()
    return redirect('products:qwikadmin_cylinders_dispatched_to_plant')

@login_required
@permission_required('users.view_admin')
def declineQwikAdminCylindersDispatchedToPlant(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.partner_confirm = False
    cylinder.who3 = "Declined"
    cylinder.who3_2 = "QwikAdmin"
    cylinder.save()
    return redirect('products:qwikadmin_cylinders_dispatched_to_plant')

@login_required
@permission_required('users.view_admin')
def acceptQwikAdminCylindersReturnedEmpty(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.vendor_confirm = True
    cylinder.who2 = "Accepted"
    cylinder.who2_2 = "QwikAdmin"
    cylinder.save()
    return redirect('products:qwikadmin_cylinders_returned_empty')

@login_required
@permission_required('users.view_admin')
def declineQwikAdminCylindersReturnedEmpty(request, id):
    cylinder = Cylinder.objects.get(id=id)
    cylinder.vendor_confirm = False
    cylinder.who2 = "Declined"
    cylinder.who2_2 = "QwikAdmin"
    cylinder.save()
    return redirect('products:qwikadmin_cylinders_returned_empty')

@login_required
@permission_required('users.view_partner')
def updateQwikPartnerCylindersReceivedEmpty(request, id):
    cylinder = Cylinder.objects.get(id=id)
    form = CylinderFormPartnerUp(instance=cylinder)
    if request.method=='POST':
        form = CylinderFormPartnerUp(request.POST, instance=cylinder)
        if form.is_valid():
            form.save()
            reg = Cylinder.objects.filter(id=cylinder.id)[0]
            reg.partner_product = request.user.first_name
            reg.save()
            messages.success(request, "The cylinder status has been modified successfully")
            return redirect('products:qwikpartner_cylinders')
    return render(request, 'products/cylinder_form_partner.html', {'form': form, 'cylinder': cylinder})

@login_required
@permission_required('users.view_partner')
def showQwikPartnerProducts(request):
    context = {}
    filtered_products = ProductFilter(
        request.GET,
        queryset = Product.objects.all()
    )
    context['filtered_products'] = filtered_products
    paginated_filtered_products = Paginator(filtered_products.qs, 10)
    page_number = request.GET.get('page')
    products_page_obj = paginated_filtered_products.get_page(page_number)
    context['products_page_obj'] = products_page_obj
    total_products = filtered_products.qs.count()
    context['total_products'] = total_products
    return render(request, 'products/qwikpartner_products.html', context=context)

@login_required
@permission_required('users.view_vendor')
def updateQwikVendorProducts(request, id):
    product = Product.objects.get(id=id)
    form = ProductForm(instance=product)
    if request.method=='POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            reg = Product.objects.filter(id=product.id)[0]
            reg.vendor_product = request.user.first_name
            reg.save()
            messages.success(request, "The product status has been modified successfully")
            return redirect('products:qwikvendor_products')
    return render(request, 'products/product_form.html', {'form': form, 'product': product})

@login_required
@permission_required('users.view_partner')
def updateQwikPartnerProducts(request, id):
    product = Product.objects.get(id=id)
    form = ProductFormPartner(instance=product)
    if request.method=='POST':
        form = ProductFormPartner(request.POST, instance=product)
        if form.is_valid():
            form.save()
            reg = Product.objects.filter(id=product.id)[0]
            reg.partner_product = request.user.first_name
            reg.save()
            messages.success(request, "The product status has been modified successfully")
            return redirect('products:qwikpartner_products')
    return render(request, 'products/product_form_partner.html', {'form': form, 'product': product})

@login_required
@permission_required('users.view_admin')
def showQwikAdminProducts(request):
    context = {}
    filtered_products = CategoryFilter(
        request.GET,
        queryset = Category.objects.all()
    )
    context['filtered_products'] = filtered_products
    paginated_filtered_products = Paginator(filtered_products.qs, 10)
    page_number = request.GET.get('page')
    products_page_obj = paginated_filtered_products.get_page(page_number)
    context['products_page_obj'] = products_page_obj
    total_products = filtered_products.qs.count()
    context['total_products'] = total_products
    return render(request, 'products/qwikadmin_products.html', context=context)

@login_required
@permission_required('users.view_admin')
def deleteProduct(request, id):
    product = Category.objects.get(id=id)
    obj = get_object_or_404(Category, id=id)
    if request.method =="POST":
        obj.delete()
        return redirect('products:qwikadmin_products')
    return render(request, 'products/qwikadmin_product_confirm_delete.html', {'product': product})

@login_required
@permission_required('users.view_admin')
def updateProduct(request, id):
    product = Category.objects.get(id=id)
    form = CategoryForm(instance=product)
    if request.method=='POST':
        form = CategoryForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "The product has been modified successfully")
            return redirect('products:qwikadmin_products')
    return render(request, 'products/qwikadmin_product_update.html', {'form': form, 'product': product})

@login_required
@permission_required('users.view_admin')
def addProduct(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, None)
        if form.is_valid():
            form.save()
            messages.success(request, "The product has been added successfully")
            return redirect('products:qwikadmin_products')
        else:
            messages.error(request, "Please review form input fields below")
    return render(request, 'products/qwikadmin_product.html', {'form': form})

#########
@login_required
@permission_required('users.view_admin')
def showQwikAdminCylinders(request):
    context = {}
    filtered_products = ProductFilterAdmin(
        request.GET,
        queryset = Product.objects.all()
    )
    context['filtered_products'] = filtered_products
    paginated_filtered_products = Paginator(filtered_products.qs, 10)
    page_number = request.GET.get('page')
    products_page_obj = paginated_filtered_products.get_page(page_number)
    context['products_page_obj'] = products_page_obj
    total_products = filtered_products.qs.count()
    context['total_products'] = total_products
    return render(request, 'products/qwikadmin_cylinders.html', context=context)

@login_required
@permission_required('users.view_admin')
def updateCylinder(request, id):
    product = Product.objects.get(id=id)
    form = ProductFormAdmin(instance=product)
    if request.method=='POST':
        form = ProductFormAdmin(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "The cylinder has been modified successfully")
            return redirect('products:qwikadmin_cylinders')
    return render(request, 'products/qwikadmin_cylinder_update.html', {'form': form, 'product': product})

@login_required
@permission_required('users.view_admin')
def addCylinder(request):
    form = ProductFormAdmin()
    if request.method == 'POST':
        form = ProductFormAdmin(request.POST, request.FILES, None)
        if form.is_valid():
            form.save()
            messages.success(request, "The cylinder has been added successfully")
            return redirect('products:qwikadmin_cylinders')
        else:
            messages.error(request, "Please review form input fields below")
    return render(request, 'products/qwikadmin_cylinder.html', {'form': form})

@login_required
@permission_required('users.view_admin')
def deleteCylinder(request, id):
    product = Product.objects.get(id=id)
    obj = get_object_or_404(Product, id=id)
    if request.method =="POST":
        obj.delete()
        return redirect('products:qwikadmin_cylinders')
    return render(request, 'products/qwikadmin_cylinder_confirm_delete.html', {'product': product})

@login_required
@permission_required('users.view_admin')
def unselectAll(request):
    reg = Product.objects.all()
    for each in reg:
        each.partner_product_status = "Unselected"
        each.save()
    messages.success(request, "All Unselected!")
    return redirect('products:qwikadmin_cylinders')
    return render(request, 'products/qwikadmin_cylinders.html')
