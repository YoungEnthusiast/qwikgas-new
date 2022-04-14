from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import OrderItem, UserOrder, OrderStatus, PayDelivery, PayLater, PaySmall
from products.models import Category, Owing, Product
from users.models import Wallet, Person, Outlet
from .filters import UserOrderFilter, UserOrderFilterSales, UserOrderFilterPayments, UserOrderFilter2, OrderItemFilter, OrderItemFilter2, OrderStatusFilter, OrderStatusFilter2
from django.contrib import messages
from django.core.mail import send_mail
from .forms import UserOrderForm, AddOrderFormVendor, ConfirmFormVendor, AddOrderFormPartner, UserOrderFormCust, PayDeliveryForm, PayLaterForm, PaySmallForm
from cart.cart import Cart
import random
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
# from django.template.loader import render_to_string
from decimal import Decimal

@login_required
def createOrder(request):
    cart = Cart(request)
    if request.method == 'POST' and request.user.is_authenticated == True:
        form = UserOrderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False).user = request.user
            # form.save(commit=False).total_cost = get_total_cost()
            try:
                reg1 = UserOrder.objects.filter(user=request.user, payment_status="Unconfirmed")[0]
                messages.error(request, "Please you cannot make a new order until you checkout the previous one in your orders below")
                return redirect('orders:orders')
            except:
                order = form.save()
                reg = UserOrder.objects.filter(user=request.user)[0]
                reg.order_Id = str(random.randint(10000000,99999999))
                reg.save()
                for item in cart:
                    OrderItem.objects.create(order=order,
                                             product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])
                cart.clear()

                reg1 = UserOrder.objects.filter(user=request.user)[0]
                reg1.total_cost = reg1.get_total_cost()
                reg1.save()
                # customer = ProductCustomer.objects.get(user=request.user)
                # first_name = customer.user.first_name
                # last_name = customer.user.last_name
                # email = form.cleaned_data.get('email')
                # send_mail(
                #     'Registered User [' + str(first_name) + ' ' + str(last_name) + ']',
                #     'Dear ' + str(first_name) + ', your order has been received. Remember you can always log in and checkout to pay from your dashboard',
                #     'admin@buildqwik.ng',
                #     [email, 'support@buildqwik.ng'],
                #     fail_silently=False,
                #     html_message = render_to_string('orders/order_email.html', {'name': str(first_name)})
                # )
                messages.success(request, "Please checkout your order on the topmost row of the orders' table below")
                return redirect('orders:orders')
        else:
            messages.error(request, "Please review form input fields below")
    else:
        form = UserOrderForm()
    return render(request, 'orders/create.html', {'cart': cart,
                                                        'form': form})

@login_required
def showOrders(request):
    context = {}
    filtered_userorders = UserOrderFilter(
        request.GET,
        queryset = UserOrder.objects.filter(user=request.user)
    )
    context['filtered_userorders'] = filtered_userorders
    paginated_filtered_userorders = Paginator(filtered_userorders.qs, 10)
    page_number = request.GET.get('page')
    userorders_page_obj = paginated_filtered_userorders.get_page(page_number)
    context['userorders_page_obj'] = userorders_page_obj
    total_userorders = filtered_userorders.qs.count()
    context['total_userorders'] = total_userorders
    return render(request, 'orders/orders.html', context=context)

@login_required
def deleteOrder(request, id):
    order = UserOrder.objects.get(id=id)
    obj = get_object_or_404(UserOrder, id=id)
    if request.method =="POST":
        obj.delete()
        return redirect('orders:orders')
    return render(request, 'orders/order_confirm_delete.html', {'order': order})

@login_required
def showOrder(request, pk, **kwargs):
    order = UserOrder.objects.get(id=pk)
    order_items = OrderItem.objects.filter(order__id=pk)

    try:
        wallet = Wallet.objects.filter(user=request.user)[0]
        current_balance = wallet.current_balance
    except:
        current_balance = 0.00

    form = PayDeliveryForm()

    if request.method == 'POST':

        form = PayDeliveryForm(request.POST, request.FILES, None)
        if form.is_valid():
            form.save(commit=False).user = request.user
            form.save()

            reg = UserOrder.objects.filter(user=request.user)[0]
            reg1 = PayDelivery.objects.filter(user=request.user)[0]
            reg.payment_type = "On Delivery"

            reg.payment_choice = reg1.payment_choice
            reg1.pay_del_Id = reg.order_Id
            reg.save()
            reg1.save()
            messages.success(request, "Your record has been saved successfully.")
            return redirect('orders:orders')

        else:
            messages.error(request, "Please review form input fields below")

    context = {'order': order, 'order_items': order_items, 'current_balance': current_balance, 'form':form}
    return render(request, 'orders/checkout.html', context)

@login_required
def addPayLater(request):
    form = PayLaterForm()
    if request.method == 'POST':
        form = PayLaterForm(request.POST, request.FILES, None)
        if form.is_valid():
            form.save(commit=False).user = request.user
            form.save()

            reg2 = UserOrder.objects.filter(user=request.user)[0]
            reg3 = PayLater.objects.filter(user=request.user)[0]
            reg2.payment_type = "Later on "
            reg2.payment_date_later = reg3.payment_date_later

            reg2.payment_choice = reg3.payment_choice
            reg3.pay_lat_Id = reg2.order_Id
            reg2.save()
            reg3.save()
            messages.success(request, "The record has been saved successfully")
            return redirect('orders:orders')
        else:
            messages.error(request, "Please review form input fields below")

    return render(request, 'orders/pay_later.html', {'form': form})

@login_required
def addPaySmall(request):
    form = PaySmallForm()
    if request.method == 'POST':
        form = PaySmallForm(request.POST, request.FILES, None)
        if form.is_valid():
            form.save(commit=False).user = request.user
            form.save()

            reg2 = UserOrder.objects.filter(user=request.user)[0]
            reg3 = PaySmall.objects.filter(user=request.user)[0]
            reg2.payment_type = "Small Small"
            reg2.payment1 = reg3.payment1
            reg2.payment2 = reg3.payment2
            reg2.payment3 = reg3.payment3
            reg2.payment1_date = reg3.payment1_date
            reg2.payment2_date = reg3.payment2_date
            reg2.payment3_date = reg3.payment3_date

            reg2.payment_choice = reg3.payment_choice
            reg3.pay_sma_Id = reg2.order_Id
            reg2.save()
            reg3.save()
            messages.success(request, "The record has been saved successfully")
            return redirect('orders:orders')
        else:
            messages.error(request, "Please review form input fields below")

    return render(request, 'orders/pay_small.html', {'form': form})

@login_required
def showInvoice(request, pk, **kwargs):
    order = UserOrder.objects.get(id=pk)
    order_items = OrderItem.objects.filter(order__id=pk)
    context = {'order': order, 'order_items': order_items}
    return render(request, 'orders/invoice.html', context)

@login_required
def showInvoiceUnPaid(request, pk, **kwargs):
    order = UserOrder.objects.get(id=pk)
    order_items = OrderItem.objects.filter(order__id=pk)
    context = {'order': order, 'order_items': order_items}
    return render(request, 'orders/invoice_unpaid.html', context)

@login_required
@permission_required('users.view_vendor')
def showQwikVendorInvoice(request, pk, **kwargs):
    order = UserOrder.objects.get(id=pk)
    order_items = OrderItem.objects.filter(order__id=pk)
    context = {'order': order, 'order_items': order_items}
    return render(request, 'orders/qwikvendor_invoice.html', context)

@login_required
@permission_required('users.view_partner')
def showQwikPartnerInvoice(request, pk, **kwargs):
    order = UserOrder.objects.get(id=pk)
    order_items = OrderItem.objects.filter(order__id=pk)
    context = {'order': order, 'order_items': order_items}
    return render(request, 'orders/qwikpartner_invoice.html', context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminInvoice(request, pk, **kwargs):
    order = UserOrder.objects.get(id=pk)
    order_items = OrderItem.objects.filter(order__id=pk)
    context = {'order': order, 'order_items': order_items}
    return render(request, 'orders/qwikadmin_invoice.html', context)

@login_required
@permission_required('users.view_vendor')
def showQwikVendorOrders(request):
    context = {}
    filtered_orders = UserOrderFilter2(
        request.GET,
        queryset = UserOrder.objects.filter(outlet__manager=request.user)
    )
    context['filtered_orders'] = filtered_orders
    paginated_filtered_orders = Paginator(filtered_orders.qs, 10)
    page_number = request.GET.get('page')
    orders_page_obj = paginated_filtered_orders.get_page(page_number)
    context['orders_page_obj'] = orders_page_obj
    total_orders = filtered_orders.qs.count()
    context['total_orders'] = total_orders
    return render(request, 'orders/qwikvendor_orders.html', context=context)

@login_required
@permission_required('users.view_partner')
def showQwikPartnerOrders(request):
    context = {}
    filtered_orders = UserOrderFilter2(
        request.GET,
        queryset = UserOrder.objects.filter(outlet__partner=request.user)
    )
    context['filtered_orders'] = filtered_orders
    paginated_filtered_orders = Paginator(filtered_orders.qs, 10)
    page_number = request.GET.get('page')
    orders_page_obj = paginated_filtered_orders.get_page(page_number)
    context['orders_page_obj'] = orders_page_obj
    total_orders = filtered_orders.qs.count()
    context['total_orders'] = total_orders
    return render(request, 'orders/qwikpartner_orders.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminOrders(request):
    context = {}
    filtered_orders = UserOrderFilter2(
        request.GET,
        queryset = UserOrder.objects.all()
    )
    context['filtered_orders'] = filtered_orders
    paginated_filtered_orders = Paginator(filtered_orders.qs, 10)
    page_number = request.GET.get('page')
    orders_page_obj = paginated_filtered_orders.get_page(page_number)
    context['orders_page_obj'] = orders_page_obj
    total_orders = filtered_orders.qs.count()
    context['total_orders'] = total_orders

    return render(request, 'orders/qwikadmin_orders.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminCredits(request):
    context = {}
    filtered_orders = UserOrderFilterSales(
        request.GET,
        queryset = UserOrder.objects.all()
    )
    context['filtered_orders'] = filtered_orders
    paginated_filtered_orders = Paginator(filtered_orders.qs, 10)
    page_number = request.GET.get('page')
    orders_page_obj = paginated_filtered_orders.get_page(page_number)
    context['orders_page_obj'] = orders_page_obj
    total_orders = filtered_orders.qs.count()
    context['total_orders'] = total_orders

    try:
        balance = UserOrder.objects.filter(payment_status="Unconfirmed").aggregate(Sum('total_cost'))['total_cost__sum']
    except:
        balance = 0
    balances = round(balance,2)

    context['balances'] = balances

    return render(request, 'orders/qwikadmin_credits.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminPayments(request):
    context = {}
    filtered_orders = UserOrderFilterPayments(
        request.GET,
        queryset = UserOrder.objects.filter(payment_status="Confirmed")
    )
    context['filtered_orders'] = filtered_orders
    paginated_filtered_orders = Paginator(filtered_orders.qs, 10)
    page_number = request.GET.get('page')
    orders_page_obj = paginated_filtered_orders.get_page(page_number)
    context['orders_page_obj'] = orders_page_obj
    total_orders = filtered_orders.qs.count()
    context['total_orders'] = total_orders

    return render(request, 'orders/qwikadmin_payments.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminSales(request):
    context = {}
    filtered_orders = UserOrderFilterSales(
        request.GET,
        queryset = UserOrder.objects.all()
    )
    context['filtered_orders'] = filtered_orders
    paginated_filtered_orders = Paginator(filtered_orders.qs, 10)
    page_number = request.GET.get('page')
    orders_page_obj = paginated_filtered_orders.get_page(page_number)
    context['orders_page_obj'] = orders_page_obj
    total_orders = filtered_orders.qs.count()
    context['total_orders'] = total_orders

    try:
        sale = UserOrder.objects.all().aggregate(Sum('total_cost'))['total_cost__sum']
    except:
        sale = 0
    # sales = round(sale,2)

    context['sale'] = sale

    return render(request, 'orders/qwikadmin_sales.html', context=context)

@login_required
def showOrderItems(request):
    context = {}
    filtered_order_items = OrderItemFilter(
        request.GET,
        queryset = OrderItem.objects.filter(order__user=request.user)
    )
    context['filtered_order_items'] = filtered_order_items
    paginated_filtered_order_items = Paginator(filtered_order_items.qs, 10)
    page_number = request.GET.get('page')
    order_items_page_obj = paginated_filtered_order_items.get_page(page_number)
    context['order_items_page_obj'] = order_items_page_obj
    total_order_items = filtered_order_items.qs.count()
    context['total_order_items'] = total_order_items
    return render(request, 'orders/order_items.html', context=context)

@login_required
@permission_required('users.view_vendor')
def showQwikVendorOrderItems(request):
    context = {}
    filtered_order_items = OrderItemFilter2(
        request.GET,
        queryset = OrderItem.objects.filter(order__outlet__manager=request.user)
    )
    context['filtered_order_items'] = filtered_order_items
    paginated_filtered_order_items = Paginator(filtered_order_items.qs, 10)
    page_number = request.GET.get('page')
    order_items_page_obj = paginated_filtered_order_items.get_page(page_number)
    context['order_items_page_obj'] = order_items_page_obj
    total_order_items = filtered_order_items.qs.count()
    context['total_order_items'] = total_order_items
    return render(request, 'orders/qwikvendor_order_items.html', context=context)

# @login_required
# @permission_required('users.view_vendor')
# def showQwikVendorOrderItems(request):
#     # outlet = Outlet.objects.filter(manager=request.user)
#     context = {}
#     filtered_order_items = OrderItemFilter2(
#         request.GET,
#         queryset = OrderItem.objects.filter(outlet_u_static=request.user.username)
#     )
#     context['filtered_order_items'] = filtered_order_items
#     paginated_filtered_order_items = Paginator(filtered_order_items.qs, 10)
#     page_number = request.GET.get('page')
#     order_items_page_obj = paginated_filtered_order_items.get_page(page_number)
#     context['order_items_page_obj'] = order_items_page_obj
#     total_order_items = filtered_order_items.qs.count()
#     context['total_order_items'] = total_order_items
#     return render(request, 'orders/qwikvendor_order_items.html', context=context)

@login_required
@permission_required('users.view_partner')
def showQwikPartnerOrderItems(request):
    context = {}
    filtered_order_items = OrderItemFilter(
        request.GET,
        queryset = OrderItem.objects.filter(order__outlet__partner=request.user)
    )
    context['filtered_order_items'] = filtered_order_items
    paginated_filtered_order_items = Paginator(filtered_order_items.qs, 10)
    page_number = request.GET.get('page')
    order_items_page_obj = paginated_filtered_order_items.get_page(page_number)
    context['order_items_page_obj'] = order_items_page_obj
    total_order_items = filtered_order_items.qs.count()
    context['total_order_items'] = total_order_items
    return render(request, 'orders/qwikpartner_order_items.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminOrderItems(request):
    context = {}
    filtered_order_items = OrderItemFilter(
        request.GET,
        queryset = OrderItem.objects.all()
    )
    context['filtered_order_items'] = filtered_order_items
    paginated_filtered_order_items = Paginator(filtered_order_items.qs, 10)
    page_number = request.GET.get('page')
    order_items_page_obj = paginated_filtered_order_items.get_page(page_number)
    context['order_items_page_obj'] = order_items_page_obj
    total_order_items = filtered_order_items.qs.count()
    context['total_order_items'] = total_order_items
    return render(request, 'orders/qwikadmin_order_items.html', context=context)

@login_required
def showOrderStatuses(request):
    context = {}
    filtered_order_statuses = OrderStatusFilter(
        request.GET,
        queryset = OrderStatus.objects.filter(order__order__user=request.user)
    )
    context['filtered_order_statuses'] = filtered_order_statuses
    paginated_filtered_order_statuses = Paginator(filtered_order_statuses.qs, 10)
    page_number = request.GET.get('page')
    order_statuses_page_obj = paginated_filtered_order_statuses.get_page(page_number)
    context['order_statuses_page_obj'] = order_statuses_page_obj
    total_order_statuses = filtered_order_statuses.qs.count()
    context['total_order_statuses'] = total_order_statuses

    out = OrderStatus.objects.filter(order__order__user=request.user, order_status="Out for Delivery").count()
    context['out'] = out
    delivered = OrderStatus.objects.filter(order__order__user=request.user, order_status="Delivered").count()
    context['delivered'] = delivered
    cancelled = OrderStatus.objects.filter(order__order__user=request.user, order_status="Cancelled").count()
    context['cancelled'] = cancelled

    return render(request, 'orders/order_statuses.html', context=context)

@login_required
@permission_required('users.view_vendor')
def showQwikVendorOrderStatuses(request):
    context = {}
    filtered_order_statuses = OrderStatusFilter2(
        request.GET,
        queryset = OrderStatus.objects.filter(order__order__outlet__manager=request.user)
    )
    context['filtered_order_statuses'] = filtered_order_statuses
    paginated_filtered_order_statuses = Paginator(filtered_order_statuses.qs, 10)
    page_number = request.GET.get('page')
    order_statuses_page_obj = paginated_filtered_order_statuses.get_page(page_number)
    context['order_statuses_page_obj'] = order_statuses_page_obj
    total_order_statuses = filtered_order_statuses.qs.count()
    context['total_order_statuses'] = total_order_statuses

    out = OrderStatus.objects.filter(order__order__outlet__manager=request.user, order_status="Out for Delivery").count()
    context['out'] = out
    delivered = OrderStatus.objects.filter(order__order__outlet__manager=request.user, order_status="Delivered").count()
    context['delivered'] = delivered
    cancelled = OrderStatus.objects.filter(order__order__outlet__manager=request.user, order_status="Cancelled").count()
    context['cancelled'] = cancelled
    return render(request, 'orders/qwikvendor_order_statuses.html', context=context)

@login_required
@permission_required('users.view_partner')
def showQwikPartnerOrderStatuses(request):
    context = {}
    filtered_order_statuses = OrderStatusFilter(
        request.GET,
        queryset = OrderStatus.objects.filter(order__order__outlet__partner=request.user)
    )
    context['filtered_order_statuses'] = filtered_order_statuses
    paginated_filtered_order_statuses = Paginator(filtered_order_statuses.qs, 10)
    page_number = request.GET.get('page')
    order_statuses_page_obj = paginated_filtered_order_statuses.get_page(page_number)
    context['order_statuses_page_obj'] = order_statuses_page_obj
    total_order_statuses = filtered_order_statuses.qs.count()
    context['total_order_statuses'] = total_order_statuses
    return render(request, 'orders/qwikpartner_order_statuses.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminOrderStatuses(request):
    context = {}
    filtered_order_statuses = OrderStatusFilter(
        request.GET,
        queryset = OrderStatus.objects.all()
    )
    context['filtered_order_statuses'] = filtered_order_statuses
    paginated_filtered_order_statuses = Paginator(filtered_order_statuses.qs, 10)
    page_number = request.GET.get('page')
    order_statuses_page_obj = paginated_filtered_order_statuses.get_page(page_number)
    context['order_statuses_page_obj'] = order_statuses_page_obj
    total_order_statuses = filtered_order_statuses.qs.count()
    context['total_order_statuses'] = total_order_statuses
    return render(request, 'orders/qwikadmin_order_statuses.html', context=context)

@login_required
@permission_required('users.view_vendor')
def addOrderStatusQwikVendor(request, id):
    order_item = OrderItem.objects.get(id=id)
    form = AddOrderFormVendor()
    if request.method == 'POST':
        form = AddOrderFormVendor(request.POST or None)
        if form.is_valid():
            product = form.cleaned_data.get('product')
            status = form.cleaned_data.get('order_status')
            form.save(commit=False).order = order_item
            form.save(commit=False).employee = request.user.first_name
            form.save()

            user = order_item.order.user
            #
            reg2 = UserOrder.objects.get(id=order_item.order.id)
            reg2.user_order_status = "Out for Delivery"
            reg2.save()

            reg = OrderStatus.objects.filter(order__order__user=user)[0]
            total = 0

            for each in reg.cylinder.all():
                total += each.category.price
            reg.static_total_cost2 = total
            reg.save()

            # email = reg.user.email
            # name = reg.user.first_name
            # order_Id = reg.order_Id
            # send_mail(
            #     'Order Status',
            #     'Dear ' + str(name) + ', Your order status has now been changed to ' + str(status),
            #     'admin@buildqwik.ng',
            #     [email, 'support@buildqwik.ng'],
            #     fail_silently=False,
            #     html_message = render_to_string('orders/add_order_email.html', {'name': str(name), 'status': str(status), 'order_Id': str(order_Id)})
            # )
            messages.success(request, "Order Status has been updated successfully")
            return redirect('orders:qwikvendor_order_items')
    return render(request, 'orders/qwikvendor_order_items_update.html', {'form': form})

@login_required
@permission_required('users.view_partner')
def addOrderStatusQwikPartner(request, id):
    order_item = OrderItem.objects.get(id=id)
    form = AddOrderFormPartner()
    if request.method == 'POST':
        form = AddOrderFormPartner(request.POST or None)
        if form.is_valid():
            product = form.cleaned_data.get('product')
            status = form.cleaned_data.get('order_status')
            form.save(commit=False).order = order_item
            form.save(commit=False).employee = request.user.first_name

            form.save()

            # reg = OrderStatus.objects.all()[0]
            # reg.order = order_item
            # reg.employee = request.user.first_name
            # reg.save()
            #
            user = order_item.order.user
            #
            reg2 = UserOrder.objects.get(id=order_item.order.id)
            reg2.user_order_status = "Delivered"
            reg2.save()

            reg = OrderStatus.objects.filter(order__order__user=user)[0]
            total = 0
            total_cylinder = ""


            for each in reg.cylinder.all():
                total += each.category.price
                total_cylinder = total_cylinder + "" + each.product_Id
            reg.static_total_cost2 = total
            reg.save()

            owing_entry = Owing()
            owing_entry.customer = user
            owing_entry.cylinder = total_cylinder
            owing_entry.save()

            owings = Owing.objects.filter(customer=user)
            reg = Person.objects.get(username=user.username)
            reg.holding = ""
            reg.save()
            reg1 = Person.objects.get(username=user.username)
            for each in owings:
                reg1.holding = reg1.holding + "" + each.cylinder
                reg1.save()

            reg4 = OrderStatus.objects.filter(order__order__user=user)[0]
            reg5 = Product.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_product_status="Unselected")

            for each1 in reg4.cylinder.all():
                for each2 in reg5:
                    if each2.product_Id == each1.product_Id:
                        each2.partner_product_status = "Selected"
                        each2.save()

            # email = reg.user.email
            # name = reg.user.first_name
            # order_Id = reg.order_Id
            # send_mail(s
            #     'Order Status',
            #     'Dear ' + str(name) + ', Your order status has now been changed to ' + str(status),
            #     'admin@buildqwik.ng',
            #     [email, 'support@buildqwik.ng'],
            #     fail_silently=False,
            #     html_message = render_to_string('orders/add_order_email.html', {'name': str(name), 'status': str(status), 'order_Id': str(order_Id)})
            # )
            messages.success(request, "Order Status has been updated successfully")
            return redirect('orders:qwikpartner_order_items')
    return render(request, 'orders/qwikpartner_order_items_update.html', {'form': form})

@login_required
def updateWallet(request, pk, **kwargs):
    order = UserOrder.objects.get(id=pk)
    order_items = OrderItem.objects.filter(order__id=pk)
    try:
        order = UserOrder.objects.get(id=pk)
        order_items = OrderItem.objects.filter(order__id=pk)
        quantity = 0
        for each in order_items:
            quantity = quantity + each.quantity
        wallet = Wallet.objects.filter(user=request.user)[0]
        wallet.current_balance = wallet.current_balance - order.get_total_cost()
        wallet.amount_debited = order.get_total_cost()
        if wallet.current_balance >= 0:
            wallet_entry = Wallet()
            wallet_entry.user = wallet.user
            wallet_entry.amount_debited = wallet.amount_debited
            wallet_entry.current_balance = wallet.current_balance
            wallet_entry.transaction_type = "Debit"
            wallet_entry.save()
            order.payment_type = "Wallet"
            order.payment_choice = " "
            order.payment_status = "Confirmed"
            try:
                order1 = UserOrder.objects.filter(user=request.user)[1]
                order.point = order1.point + quantity
                order.save()
            except:
                order.point = quantity
                order.save()
            order3 = UserOrder.objects.get(id=pk)
            if order3.point >= 11:
                category = Category.objects.all().order_by('price')[0]
                price = category.price
                point_perc = Decimal(0.05) * price
                try:
                    wallet2 = Wallet.objects.filter(user=request.user)[0]
                    current_balance2 = wallet2.current_balance
                    wallet_entry3 = Wallet()
                    wallet_entry3.user = request.user
                    wallet_entry3.point = point_perc
                    wallet_entry3.current_balance = current_balance2 + point_perc
                    wallet_entry3.transaction_type = "QwikPoint"
                    wallet_entry3.save()
                except:
                    current_balance2 = 0
                    wallet_entry3 = Wallet()
                    wallet_entry3.user = request.user
                    wallet_entry3.first = point_perc
                    wallet_entry3.current_balance = current_balance2 + ref_perc
                    wallet_entry3.transaction_type = "QwikPoint"
                    wallet_entry3.save()
                order3.point = order3.point - 11
                order3.save()
            user = order.user
            referrer = order.user.referrer
            count = UserOrder.objects.filter(payment_status="Confirmed", user=user).count()
            if count == 1:
                #total_paid = order.get_total_cost()
                category = Category.objects.all().order_by('price')[0]
                price = category.price
                ref_perc = Decimal(0.05) * price
                try:
                    person2 = Person.objects.get(username=referrer)
                except:
                    person2 = None
                try:
                    wallet0 = Wallet.objects.filter(user=person2)[0]
                    current_balance = wallet0.current_balance
                    wallet_entry2 = Wallet()
                    wallet_entry2.user = person2
                    wallet_entry2.referral = ref_perc
                    wallet_entry2.current_balance = current_balance + ref_perc
                    wallet_entry2.transaction_type = "QwikReferral"
                    wallet_entry2.save()
                except:
                    current_balance = 0
                    wallet_entry2 = Wallet()
                    wallet_entry2.user = person2
                    wallet_entry2.referral = ref_perc
                    wallet_entry2.current_balance = current_balance + ref_perc
                    wallet_entry2.transaction_type = "QwikReferral"
                    wallet_entry2.save()
                try:
                    wallet1 = Wallet.objects.filter(user=request.user)[0]
                    current_balance1 = wallet1.current_balance
                    wallet_entry1 = Wallet()
                    wallet_entry1.user = request.user
                    wallet_entry1.first = ref_perc
                    wallet_entry1.current_balance = current_balance1 + ref_perc
                    wallet_entry1.transaction_type = "QwikFirst"
                    wallet_entry1.save()
                except:
                    current_balance1 = 0
                    wallet_entry1 = Wallet()
                    wallet_entry1.user = request.user
                    wallet_entry1.first = ref_perc
                    wallet_entry1.current_balance = current_balance1 + ref_perc
                    wallet_entry1.transaction_type = "QwikFirst"
                    wallet_entry1.save()
            return render(request, 'orders/payment_card.html', {'order': order, 'order_items': order_items})
        else:
            messages.error(request, "Wallet balance is not enough to perform this transaction. Please fund your wallet")
            return render(request, 'orders/checkout.html', {'order': order, 'order_items': order_items})
    except:
        messages.error(request, "Wallet balance is not enough to perform this transaction. Please fund your wallet")
        return render(request, 'orders/checkout.html', {'order': order, 'order_items': order_items})

def showPaymentComplete(request):
    order = UserOrder.objects.filter(user=request.user)[0]
    order.payment_type = "Wallet"
    order.payment_choice = " "
    order.payment_status = "Confirmed"
    order.save()
    user = order.user
    referrer = order.user.referrer
    count = UserOrder.objects.filter(payment_status="Confirmed", user=user).count()
    if count == 1:
        #total_paid = order.get_total_cost()
        category = Category.objects.all().order_by('price')[0]
        price = category.price
        ref_perc = Decimal(0.05) * price
        try:
            person2 = Person.objects.get(username=referrer)
        except:
            person2 = None
        try:
            wallet0 = Wallet.objects.filter(user=person2)[0]
            current_balance = wallet0.current_balance
            wallet_entry = Wallet()
            wallet_entry.user = person2
            wallet_entry.referral = ref_perc
            wallet_entry.current_balance = current_balance + ref_perc
            wallet_entry.transaction_type = "QwikReferral"
            wallet_entry.save()
        except:
            current_balance = 0
            wallet_entry = Wallet()
            wallet_entry.user = person2
            wallet_entry.referral = ref_perc
            wallet_entry.current_balance = current_balance + ref_perc
            wallet_entry.transaction_type = "QwikReferral"
            wallet_entry.save()
        try:
            wallet1 = Wallet.objects.filter(user=request.user)[0]
            current_balance1 = wallet1.current_balance
            wallet_entry1 = Wallet()
            wallet_entry1.user = request.user
            wallet_entry1.first = ref_perc
            wallet_entry1.current_balance = current_balance1 + ref_perc
            wallet_entry1.transaction_type = "QwikFirst"
            wallet_entry1.save()
        except:
            current_balance1 = 0
            wallet_entry1 = Wallet()
            wallet_entry1.user = request.user
            wallet_entry1.first = ref_perc
            wallet_entry1.current_balance = current_balance1 + ref_perc
            wallet_entry1.transaction_type = "QwikFirst"
            wallet_entry1.save()
    pk = order.id
    order_items = OrderItem.objects.filter(order__id=pk)
    order = UserOrder.objects.get(id=pk)
    order_items = OrderItem.objects.filter(order__id=pk)
    quantity = 0
    for each in order_items:
        quantity = quantity + each.quantity
    try:
        order1 = UserOrder.objects.filter(user=request.user)[1]
        order.point = order1.point + quantity
        order.save()
    except:
        order.point = quantity
        order.save()
    order3 = UserOrder.objects.get(id=pk)
    if order3.point >= 11:
        category = Category.objects.all().order_by('price')[0]
        price = category.price
        point_perc = Decimal(0.05) * price
        try:
            wallet2 = Wallet.objects.filter(user=request.user)[0]
            current_balance2 = wallet2.current_balance
            wallet_entry3 = Wallet()
            wallet_entry3.user = request.user
            wallet_entry3.point = point_perc
            wallet_entry3.current_balance = current_balance2 + point_perc
            wallet_entry3.transaction_type = "QwikPoint"
            wallet_entry3.save()
        except:
            current_balance2 = 0
            wallet_entry3 = Wallet()
            wallet_entry3.user = request.user
            wallet_entry3.first = point_perc
            wallet_entry3.current_balance = current_balance2 + ref_perc
            wallet_entry3.transaction_type = "QwikPoint"
            wallet_entry3.save()
        order3.point = order3.point - 11
        order3.save()
    return render(request, 'orders/payment_card.html')

@login_required
def showAddressCust(request, id):
    order = UserOrder.objects.get(id=id)
    form = UserOrderFormCust(instance=order)
    if request.method == 'POST':
        form = UserOrderFormCust(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            # messages.success(request, "Order Status has been updated successfully")
            # return redirect('orders:qwikvendor_order_items')
    return render(request, 'orders/qwikcustomer_address.html', {'form': form})

@login_required
@permission_required('users.view_vendor')
def confirmOrderVendor(request, id):
    order = UserOrder.objects.get(id=id)
    form = ConfirmFormVendor(instance=order)
    if request.method=='POST':
        form = ConfirmFormVendor(request.POST, instance=order)
        if form.is_valid():
            form.save()
            order2 = UserOrder.objects.get(id=id)
            order2.payment_type = "QwikVendor"
            # order2.payment_choice = order
            order2.payment_status = "Confirmed"
            order2.save()
            user = order2.user
            referrer = order2.user.referrer
            count = UserOrder.objects.filter(payment_status="Confirmed", user=user).count()

            if count == 1:
                #total_paid = order.get_total_cost()
                category = Category.objects.all().order_by('price')[0]
                price = category.price
                ref_perc = Decimal(0.05) * price
                try:
                    person2 = Person.objects.get(username=referrer)
                except:
                    person2 = None
                try:
                    wallet0 = Wallet.objects.filter(user=person2)[0]
                    current_balance = wallet0.current_balance
                    wallet_entry = Wallet()
                    wallet_entry.user = person2
                    wallet_entry.referral = ref_perc
                    wallet_entry.current_balance = current_balance + ref_perc
                    wallet_entry.transaction_type = "QwikReferral"
                    wallet_entry.save()
                except:
                    current_balance = 0
                    wallet_entry = Wallet()
                    wallet_entry.user = person2
                    wallet_entry.referral = ref_perc
                    wallet_entry.current_balance = current_balance + ref_perc
                    wallet_entry.transaction_type = "QwikReferral"
                    wallet_entry.save()
                try:
                    wallet1 = Wallet.objects.filter(user=user)[0]
                    current_balance1 = wallet1.current_balance
                    wallet_entry1 = Wallet()
                    wallet_entry1.user = user
                    wallet_entry1.first = ref_perc
                    wallet_entry1.current_balance = current_balance1 + ref_perc
                    wallet_entry1.transaction_type = "QwikFirst"
                    wallet_entry1.save()
                except:
                    current_balance1 = 0
                    wallet_entry1 = Wallet()
                    wallet_entry1.user = user
                    wallet_entry1.first = ref_perc
                    wallet_entry1.current_balance = current_balance1 + ref_perc
                    wallet_entry1.transaction_type = "QwikFirst"
                    wallet_entry1.save()
            pk = order.id
            order_items = OrderItem.objects.filter(order__id=pk)
            order = UserOrder.objects.get(id=pk)
            order_items = OrderItem.objects.filter(order__id=pk)
            quantity = 0
            for each in order_items:
                quantity = quantity + each.quantity
            try:
                order1 = UserOrder.objects.filter(user=user)[1]
                order.point = order1.point + quantity
                order.save()
            except:
                order.point = quantity
                order.save()
            order3 = UserOrder.objects.get(id=pk)
            if order3.point >= 11:
                category = Category.objects.all().order_by('price')[0]
                price = category.price
                point_perc = Decimal(0.05) * price
                try:
                    wallet2 = Wallet.objects.filter(user=user)[0]
                    current_balance2 = wallet2.current_balance
                    wallet_entry3 = Wallet()
                    wallet_entry3.user = user
                    wallet_entry3.point = point_perc
                    wallet_entry3.current_balance = current_balance2 + point_perc
                    wallet_entry3.transaction_type = "QwikPoint"
                    wallet_entry3.save()
                except:
                    current_balance2 = 0
                    wallet_entry3 = Wallet()
                    wallet_entry3.user = user
                    wallet_entry3.first = point_perc
                    wallet_entry3.current_balance = current_balance2 + ref_perc
                    wallet_entry3.transaction_type = "QwikPoint"
                    wallet_entry3.save()
                order3.point = order3.point - 11
                order3.save()

            messages.success(request, "The order has been confirmed successfully")
            return redirect('orders:qwikvendor_orders')
    return render(request, 'orders/qwikvendor_order_confirm.html', {'form': form, 'order': order})
