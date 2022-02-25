from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, Cylinder
from orders.models import UserOrder
from users.models import Wallet
from .forms import CategoryForm, ProductForm, ProductFormPartner, ProductFormAdmin, CylinderFormVendor, CylinderFormAdminUp, CylinderFormPartner, CylinderFormVendorUp, CylinderFormPartnerUp, CylinderFormCustomerUp
# from orders.forms import VisitorOrderForm
from .filters import ProductFilter, ProductFilterAdmin, CategoryFilter, CylinderFilter
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
from users.models import Person

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
def showQwikCustomerCylinders(request):
    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = Cylinder.objects.filter(customer=request.user)
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders
    return render(request, 'products/qwikcustomer_cylinders.html', context=context)

@login_required
@permission_required('users.view_vendor')
def showQwikVendorCylinders(request):
    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = Cylinder.objects.filter(cylinder__outlet__manager=request.user)
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders
    return render(request, 'products/qwikvendor_cylinders.html', context=context)

@login_required
@permission_required('users.view_partner')
def showQwikPartnerCylinders(request):
    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = Cylinder.objects.filter(cylinder__outlet__partner=request.user)
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders
    return render(request, 'products/qwikpartner_cylinders.html', context=context)

@login_required
@permission_required('users.view_partner')
def showQwikPartnerCylindersReceivedEmpty(request):
    cylinders = Cylinder.objects.all().count()
    received_empty_from_qwikcustomers = Cylinder.objects.filter(partner_product_status="Received Empty from QwikCustomer").count()
    returned_empty_to_qwiklets = Cylinder.objects.filter(partner_product_status="Returned Empty to QwikLet").count()
    dispatched_to_plants = Cylinder.objects.filter(partner_product_status="Dispatched to Plant").count()
    delivered_filled_to_qwiklets = Cylinder.objects.filter(partner_product_status="Delivered Filled to QwikLet").count()
    dispatched_filled_to_qwikcustomers = Cylinder.objects.filter(partner_product_status="Dispatched Filled to QwikCustomer").count()
    delivered_to_qwikcustomers = Cylinder.objects.filter(partner_product_status="Delivered to QwikCustomer").count()
    returned_filled_to_qwiklets = Cylinder.objects.filter(partner_product_status="Returned Filled to QwikLet").count()

    perc_received_empty_from_qwikcustomers = round((received_empty_from_qwikcustomers/cylinders)*100,1)
    perc_returned_empty_to_qwiklets = round((returned_empty_to_qwiklets/cylinders)*100,1)
    perc_dispatched_to_plants = round((dispatched_to_plants/cylinders)*100,1)
    perc_delivered_filled_to_qwiklets = round((delivered_filled_to_qwiklets/cylinders)*100,1)
    perc_dispatched_filled_to_qwikcustomers = round((dispatched_filled_to_qwikcustomers/cylinders)*100,1)
    perc_delivered_to_qwikcustomers = round((delivered_to_qwikcustomers/cylinders)*100,1)
    perc_returned_filled_to_qwiklets = round((returned_filled_to_qwiklets/cylinders)*100,1)

    received_empty_from_qwikcustomer = round(perc_received_empty_from_qwikcustomers/100,2)
    returned_empty_to_qwiklet = round(perc_returned_empty_to_qwiklets/100,2)
    dispatched_to_plant = round(perc_dispatched_to_plants/100,2)
    delivered_filled_to_qwiklet = round(perc_delivered_filled_to_qwiklets/100,2)
    dispatched_filled_to_qwikcustomer = round(perc_dispatched_filled_to_qwikcustomers/100,2)
    delivered_to_qwikcustomer = round(perc_delivered_to_qwikcustomers/100,2)
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
    context['returned_filled_to_qwiklets'] = returned_filled_to_qwiklets

    context['perc_received_empty_from_qwikcustomers'] = perc_received_empty_from_qwikcustomers
    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets
    context['perc_dispatched_to_plants'] = perc_dispatched_to_plants
    context['perc_delivered_filled_to_qwiklets'] = perc_delivered_filled_to_qwiklets
    context['perc_dispatched_filled_to_qwikcustomers'] = perc_dispatched_filled_to_qwikcustomers
    context['perc_delivered_to_qwikcustomers'] = perc_delivered_to_qwikcustomers
    context['perc_returned_filled_to_qwiklets'] = perc_returned_filled_to_qwiklets

    context['received_empty_from_qwikcustomer'] = received_empty_from_qwikcustomer
    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet
    context['dispatched_to_plant'] = dispatched_to_plant
    context['delivered_filled_to_qwiklet'] = delivered_filled_to_qwiklet
    context['dispatched_filled_to_qwikcustomer'] = dispatched_filled_to_qwikcustomer
    context['delivered_to_qwikcustomer'] = delivered_to_qwikcustomer
    context['returned_filled_to_qwiklet'] = returned_filled_to_qwiklet

    form = CylinderFormPartner()
    if request.method == 'POST':
        form = CylinderFormPartner(request.POST, request.FILES, None)
        if form.is_valid():
            cylinder = form.cleaned_data.get('cylinder')
            try:
                product = Product.objects.filter(product_Id=cylinder)[0]
                category = product.category.type
            except:
                category = "None"
            form.save(commit=False).partner_product_status = "Received Empty from QwikCustomer"
            form.save(commit=False).category = category
            form.save()
            messages.success(request, "The cylinder stage has been added successfully")
            return redirect('products:qwikpartner_cylinders_received_empty')
        else:
            messages.error(request, "Please review form input fields below")
    context['form'] = form
    return render(request, 'products/qwikpartner_cylinders_received_empty.html', context=context)

@login_required
@permission_required('users.view_partner')
def showQwikCustomerCylindersReturnedEmpty(request):
    cylinders = Cylinder.objects.all().count()
    returned_empty_to_qwikpartners = Cylinder.objects.filter(customer_product_status="Returned Empty to QwikPartner").count()
    received_filleds = Cylinder.objects.filter(customer_product_status="Received Filled").count()

    perc_returned_empty_to_qwikpartners = round((returned_empty_to_qwikpartners/cylinders)*100,1)
    perc_received_filleds = round((received_filleds/cylinders)*100,1)

    returned_empty_to_qwikpartner = round(perc_received_empty_from_qwikcustomers/100,2)
    received_filled = round(perc_received_filleds/100,2)

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

    context['perc_received_empty_from_qwikcustomers'] = perc_received_empty_from_qwikcustomers
    context['perc_returned_empty_to_qwiklets'] = perc_returned_empty_to_qwiklets

    context['received_empty_from_qwikcustomer'] = received_empty_from_qwikcustomer
    context['returned_empty_to_qwiklet'] = returned_empty_to_qwiklet

    form = CylinderFormPartner()
    if request.method == 'POST':
        form = CylinderFormPartner(request.POST, request.FILES, None)
        if form.is_valid():
            cylinder = form.cleaned_data.get('cylinder')
            try:
                product = Product.objects.filter(product_Id=cylinder)[0]
                category = product.category.type
            except:
                category = "None"
            form.save(commit=False).partner_product_status = "Received Empty from QwikCustomer"
            form.save(commit=False).category = category
            form.save()
            messages.success(request, "The cylinder stage has been added successfully")
            return redirect('products:qwikpartner_cylinders_received_empty')
        else:
            messages.error(request, "Please review form input fields below")
    context['form'] = form
    return render(request, 'products/qwikcustomer_cylinders_returned_empty.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminAdmCylinders(request):
    context = {}
    filtered_cylinders = CylinderFilter(
        request.GET,
        queryset = Cylinder.objects.all()
    )
    context['filtered_cylinders'] = filtered_cylinders
    paginated_filtered_cylinders = Paginator(filtered_cylinders.qs, 10)
    page_number = request.GET.get('page')
    cylinders_page_obj = paginated_filtered_cylinders.get_page(page_number)
    context['cylinders_page_obj'] = cylinders_page_obj
    total_cylinders = filtered_cylinders.qs.count()
    context['total_cylinders'] = total_cylinders
    return render(request, 'products/qwikadmin_adm_cylinders.html', context=context)

@login_required
@permission_required('users.view_vendor')
def updateQwikVendorCylinders(request, id):
    cylinder = Cylinder.objects.get(id=id)
    form = CylinderFormVendorUp(instance=cylinder)
    if request.method=='POST':
        form = CylinderFormVendorUp(request.POST, instance=cylinder)
        if form.is_valid():
            form.save()
            reg = Cylinder.objects.filter(id=cylinder.id)[0]
            reg.vendor_product = request.user.first_name
            reg.save()
            messages.success(request, "The cylinder status has been modified successfully")
            return redirect('products:qwikvendor_cylinders')
    return render(request, 'products/cylinder_form.html', {'form': form, 'cylinder': cylinder})

@login_required
@permission_required('users.view_admin')
def updateQwikAdminAdmCylinders(request, id):
    cylinder = Cylinder.objects.get(id=id)
    form = CylinderFormAdminUp(instance=cylinder)
    if request.method=='POST':
        form = CylinderFormAdminUp(request.POST, instance=cylinder)
        if form.is_valid():
            form.save()
            reg = Cylinder.objects.filter(id=cylinder.id)[0]
            reg.admin_product = request.user.first_name
            reg.save()
            messages.success(request, "The cylinder status has been modified successfully")
            return redirect('products:qwikadmin_adm_cylinders')
    return render(request, 'products/cylinder_form_admin.html', {'form': form, 'cylinder': cylinder})

@login_required
def updateQwikCustomerCylinders(request, id):
    cylinder = Cylinder.objects.get(id=id)
    form = CylinderFormCustomerUp(instance=cylinder)
    if request.method=='POST':
        form = CylinderFormCustomerUp(request.POST, instance=cylinder)
        if form.is_valid():
            form.save()
            reg = Cylinder.objects.filter(id=cylinder.id)[0]
            reg.customer_product = request.user.first_name
            reg.save()
            messages.success(request, "The cylinder status has been modified successfully")
            return redirect('products:qwikcustomer_cylinders')
    return render(request, 'products/cylinder_form_customer.html', {'form': form, 'cylinder': cylinder})

@login_required
@permission_required('users.view_partner')
def updateQwikPartnerCylinders(request, id):
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
@permission_required('users.view_vendor')
def addQwikVendorCylinder(request):
    form = CylinderFormVendor()
    if request.method == 'POST':
        form = CylinderFormVendor(request.POST, request.FILES, None)
        if form.is_valid():
            form.save()
            messages.success(request, "The cylinder has been added successfully")
            return redirect('products:qwikvendor_cylinders')
        else:
            messages.error(request, "Please review form input fields below")
    return render(request, 'products/qwikvendor_cylinder.html', {'form': form})

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
def deleteCylinder(request, id):
    product = Product.objects.get(id=id)
    obj = get_object_or_404(Product, id=id)
    if request.method =="POST":
        obj.delete()
        return redirect('products:qwikadmin_cylinders')
    return render(request, 'products/qwikadmin_cylinder_confirm_delete.html', {'product': product})

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
