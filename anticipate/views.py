from django.shortcuts import render, redirect
from users.models import Outlet
from .models import AntiOrder#, OrderStatus
# from products.models import Category
# from users.models import Wallet, Person, Outlet
from .filters import AntiOrderFilter, AntiOrderFilter2#, OrderItemFilter, OrderItemFilter2, OrderStatusFilter, OrderStatusFilter2
from django.contrib import messages
# from django.core.mail import send_mail
from .forms import AntiOrderForm, AntiOrderFormVen, AntiOrderFormPar, AntiOrderFormPar2
import random
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
# from django.template.loader import render_to_string
# from decimal import Decimal

@login_required
def showAntiOrders(request):
    context = {}
    filtered_antiorders = AntiOrderFilter(
        request.GET,
        queryset = AntiOrder.objects.filter(user=request.user)
    )
    context['filtered_antiorders'] = filtered_antiorders
    paginated_filtered_antiorders = Paginator(filtered_antiorders.qs, 10)
    page_number = request.GET.get('page')
    antiorders_page_obj = paginated_filtered_antiorders.get_page(page_number)
    context['antiorders_page_obj'] = antiorders_page_obj
    total_antiorders = filtered_antiorders.qs.count()
    context['total_antiorders'] = total_antiorders
    return render(request, 'anticipate/anti_orders.html', context=context)

@login_required
@permission_required('users.view_vendor')
def showQwikVendorAntiOrders(request):
    context = {}
    filtered_antiorders = AntiOrderFilter2(
        request.GET,
        queryset = AntiOrder.objects.filter(outlet__manager=request.user)
    )
    context['filtered_antiorders'] = filtered_antiorders
    paginated_filtered_antiorders = Paginator(filtered_antiorders.qs, 10)
    page_number = request.GET.get('page')
    antiorders_page_obj = paginated_filtered_antiorders.get_page(page_number)
    context['antiorders_page_obj'] = antiorders_page_obj
    total_antiorders = filtered_antiorders.qs.count()
    context['total_antiorders'] = total_antiorders
    return render(request, 'anticipate/qwikvendor_anti_orders.html', context=context)

@login_required
@permission_required('users.view_partner')
def showQwikPartnerAntiOrders(request):
    context = {}
    filtered_antiorders = AntiOrderFilter2(
        request.GET,
        queryset = AntiOrder.objects.filter(outlet__partner=request.user)
    )
    context['filtered_antiorders'] = filtered_antiorders
    paginated_filtered_antiorders = Paginator(filtered_antiorders.qs, 10)
    page_number = request.GET.get('page')
    antiorders_page_obj = paginated_filtered_antiorders.get_page(page_number)
    context['antiorders_page_obj'] = antiorders_page_obj
    total_antiorders = filtered_antiorders.qs.count()
    context['total_antiorders'] = total_antiorders

    form = AntiOrderForm()
    if request.method == 'POST':
        form = AntiOrderForm(request.POST, request.FILES, None)
        if form.is_valid():
            outlet = Outlet.objects.get(partner=request.user)
            form.save(commit=False).outlet = outlet
            form.save(commit=False).order_Id = str(random.randint(10000000,99999999))
            form.save()
            user = form.cleaned_data.get('user')
            reg = AntiOrder.objects.filter(user=user)[0]
            reg.static_price = reg.product.category.price
            reg.static_total_cost = reg.total_cost()
            reg.save()

            # form.save()
            messages.success(request, "The anticipatory order has been added successfully")
            return redirect('anticipate:qwikpartner_anti_orders')
        else:
            messages.error(request, "Please review form input fields below")
    context['form'] = form
    return render(request, 'anticipate/qwikpartner_anti_orders.html', context=context)

@login_required
@permission_required('users.view_partner')
def updateQwikPartnerAntiOrders(request, id):
    order = AntiOrder.objects.get(id=id)
    form = AntiOrderFormPar(instance=order)
    if request.method=='POST':
        form = AntiOrderFormPar(request.POST, instance=order)
        if form.is_valid():
            form.save()
            # reg = AntiOrder.objects.filter(id=product.id)[0]
            # reg.vendor_product = request.user.first_name
            # reg.save()
            messages.success(request, "The order has been modified successfully")
            return redirect('anticipate:qwikpartner_anti_orders')
    return render(request, 'anticipate/qwikpartner_anti_order_update.html', {'form': form, 'order': order})

@login_required
@permission_required('users.view_partner')
def updateQwikPartnerAntiOrders3rd(request, id):
    order = AntiOrder.objects.get(id=id)
    form = AntiOrderFormPar2(instance=order)
    if request.method=='POST':
        form = AntiOrderFormPar2(request.POST, instance=order)
        if form.is_valid():
            form.save()
            # reg = AntiOrder.objects.filter(id=product.id)[0]
            # reg.vendor_product = request.user.first_name
            # reg.save()
            messages.success(request, "The order has been modified successfully")
            return redirect('anticipate:qwikpartner_anti_orders')
    return render(request, 'anticipate/qwikpartner_anti_order_update_2.html', {'form': form, 'order': order})

@login_required
@permission_required('users.view_vendor')
def updateQwikVendorAntiOrders(request, id):
    order = AntiOrder.objects.get(id=id)
    form = AntiOrderFormVen(instance=order)
    if request.method=='POST':
        form = AntiOrderFormVen(request.POST, instance=order)
        if form.is_valid():
            form.save()
            # reg = AntiOrder.objects.filter(id=product.id)[0]
            # reg.vendor_product = request.user.first_name
            # reg.save()
            messages.success(request, "The order has been modified successfully")
            return redirect('anticipate:qwikvendor_anti_orders')
    return render(request, 'anticipate/qwikvendor_anti_order_update.html', {'form': form, 'order': order})

# @login_required
# @permission_required('users.view_partner')
# def addQwikPartnerAntiOrder(request):
#     form = AntiOrderForm()
#     if request.method == 'POST':
#         form = AntiOrderForm(request.POST, request.FILES, None)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "The anticipatory order has been added successfully")
#             return redirect('anticipate:qwikpartner_anti_orders')
#         else:
#             messages.error(request, "Please review form input fields below")
#     return render(request, 'anticipate/qwikpartner_anti_order.html', {'form': form})

@login_required
@permission_required('users.view_partner')
def showQwikPartnerAntiInvoice(request, pk, **kwargs):
    order = AntiOrder.objects.get(id=pk)
    # order_items = OrderItem.objects.filter(order__id=pk)
    context = {'order': order}#, 'order_items': order_items}
    return render(request, 'anticipate/qwikpartner_anti_invoice.html', context)

@login_required
@permission_required('users.view_vendor')
def showQwikVendorAntiInvoice(request, pk, **kwargs):
    order = AntiOrder.objects.get(id=pk)
    # order_items = OrderItem.objects.filter(order__id=pk)
    context = {'order': order}#, 'order_items': order_items}
    return render(request, 'anticipate/qwikvendor_anti_invoice.html', context)

@login_required
def showAntiInvoice(request, pk, **kwargs):
    order = AntiOrder.objects.get(id=pk)
    # order_items = OrderItem.objects.filter(order__id=pk)
    context = {'order': order}#, 'order_items': order_items}
    return render(request, 'anticipate/anti_invoice.html', context)
