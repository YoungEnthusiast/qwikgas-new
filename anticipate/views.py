from django.shortcuts import render, redirect, get_object_or_404
from users.models import Outlet, Person
from .models import AntiOrder
from orders.models import UserOrder
from products.models import Owing, Product, Cylinder
# from products.models import Category
# from users.models import Wallet, Person, Outlet
from .filters import AntiOrderFilter, AntiOrderFilter2, AntiOrderFilterSales, AntiOrderFilterCredits, AntiOrderFilterPayments
from django.contrib import messages
# from django.core.mail import send_mail
from .forms import AntiOrderForm, AntiOrderFormVen, AntiOrderFormPar, AntiOrderFormPar2
from django.forms import inlineformset_factory
import random
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.template.loader import render_to_string
import csv
from django.http import HttpResponse
# from weasyprint import HTML, CSS
import tempfile
import datetime
#
# import os
#
# os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")
#
# from weasyprint import HTML, CSS

# HTML('https://weasyprint.org/').write_pdf('weasyprint-website.pdf')
#
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context



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

            user = form.cleaned_data.get('user')
            cylinder = form.cleaned_data.get('cylinder')

            payment1 = form.cleaned_data.get('payment1')
            payment2 = form.cleaned_data.get('payment2')
            payment3 = form.cleaned_data.get('payment3')

            x = datetime.datetime.now().year + datetime.datetime.now().month + datetime.datetime.now().day + datetime.datetime.now().hour + datetime.datetime.now().minute + datetime.datetime.now().second + 50*datetime.datetime.now().microsecond


            form.save(commit=False).outlet = outlet
            form.save(commit=False).order_Id = x
            form.save(commit=False).payment_total = payment1
            form.save(commit=False).stage = "1st"

            form.save()

            reg = AntiOrder.objects.filter(user=user)[0]
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
            reg2 = Person.objects.get(username=user.username)
            reg2.holding = ""
            reg2.save()
            reg1 = Person.objects.get(username=user.username)
            for each in owings:
                reg1.holding = reg1.holding + "" + each.cylinder
                reg1.save()

            reg3 = AntiOrder.objects.filter(user=user)[0]
            reg3.balance = reg3.static_total_cost2 - reg3.payment_total
            reg3.save()


            reg4 = AntiOrder.objects.filter(user=user)[0]
            reg5 = Product.objects.filter(vendor_product_status="Released Filled to QwikPartner", partner_product_status="Unselected")

            for each1 in reg4.cylinder.all():
                for each2 in reg5:
                    if each2.product_Id == each1.product_Id:
                        each2.partner_product_status = "Selected"
                        each2.save()

            messages.success(request, "The anticipatory order has been added successfully")
            return redirect('anticipate:qwikpartner_anti_orders')
        else:
            messages.error(request, "Please review form input fields below")
    context['form'] = form
    return render(request, 'anticipate/qwikpartner_anti_orders.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminAntiOrders(request):
    context = {}
    filtered_antiorders = AntiOrderFilter2(
        request.GET,
        queryset = AntiOrder.objects.all()
    )
    context['filtered_antiorders'] = filtered_antiorders
    paginated_filtered_antiorders = Paginator(filtered_antiorders.qs, 10)
    page_number = request.GET.get('page')
    antiorders_page_obj = paginated_filtered_antiorders.get_page(page_number)
    context['antiorders_page_obj'] = antiorders_page_obj
    total_antiorders = filtered_antiorders.qs.count()
    context['total_antiorders'] = total_antiorders

    return render(request, 'anticipate/qwikadmin_anti_orders.html', context=context)

@login_required
@permission_required('users.view_admin')
def randomize(request):
    reg = AntiOrder.objects.all()
    for each in reg:
        each.order_Id = random.randint(10000000,99999999)
        each.save()
    messages.success(request, "Orders Randomized!")
    return redirect('anticipate:qwikadmin_randomize')
    return render(request, 'anticipate/qwikadmin_anti_orders.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminSalesGraph(request):
    sales = AntiOrder.objects.all().order_by('created')
    created_list = [""]
    static_total_cost2_list = [0]
    # total = 0.00
    for each in sales:
        if each.created.strftime('%d, %b %Y') in created_list:
            total = static_total_cost2_list[-1]
            try:
                total = int(total) + int(each.static_total_cost2)
                static_total_cost2_list.pop()
                static_total_cost2_list.append(int(total))
            except:
                each.static_total_cost2 = 0
                total = int(total) + int(each.static_total_cost2)
                static_total_cost2_list.pop()
                static_total_cost2_list.append(int(total))
        else:
            created_list.append(each.created.strftime('%d, %b %Y'))
            try:
                static_total_cost2_list.append(int(each.static_total_cost2))
            except:
                each.static_total_cost2 = 0
                static_total_cost2_list.append(int(each.static_total_cost2))
    sales_user = UserOrder.objects.all().order_by('created')
    created_user_list = [""]
    total_cost_list = [0]
    # total = 0.00
    for each_user in sales_user:
        if each_user.created.strftime('%d, %b %Y') in created_user_list:
            total_user = total_cost_list[-1]
            try:
                total_user = int(total_user) + int(each_user.total_cost)
                total_cost_list.pop()
                total_cost_list.append(int(total_user))
            except:
                each_user.total_cost = 0
                total_user = int(total_user) + int(each_user.total_cost)
                total_cost_list.pop()
                total_cost_list.append(int(total_user))

        else:
            created_user_list.append(each_user.created.strftime('%d, %b %Y'))
            try:
                total_cost_list.append(int(each_user.total_cost))
            except:
                each_user.total_cost = 0
                total_cost_list.append(int(each_user.total_cost))

    sales_joint = AntiOrder.objects.all().order_by('created')
    created_joint_list = [""]
    total_joint_cost_list = [0]
    # total = 0.00

    counter = -1
    for each_joint in sales_joint:
        if each_joint.created.strftime('%d, %b %Y') in created_joint_list:
            total_joint = total_joint_cost_list[-1]
            try:
                total_joint = int(total_joint) + int(each_joint.static_total_cost2)
                total_joint_cost_list.pop()
                total_joint_cost_list.append(int(total_joint))
            except:
                each_joint.static_total_cost2 = 0
                total_joint = int(total_joint) + int(each_joint.static_total_cost2)
                total_joint_cost_list.pop()
                total_joint_cost_list.append(int(total_joint))
        else:
            counter += 1
            created_joint_list.append(each_joint.created.strftime('%d, %b %Y'))
            try:
                total_joint_cost_list.append(int(each_joint.static_total_cost2))
            except:
                each_joint.static_total_cost2 = 0
                total_joint_cost_list.append(int(each_joint.static_total_cost2))

    sales_joint2 = UserOrder.objects.all().order_by('created')

    for each_joint2 in sales_joint2:
        if each_joint2.created.strftime('%d, %b %Y') in created_joint_list:
            d_index = created_joint_list.index(each_joint2.created.strftime('%d, %b %Y'))
            total_joint2 = total_joint_cost_list[d_index]
            try:
                total_joint2 = int(total_joint2) + int(each_joint2.total_cost)
            except:
                each_joint2.total_cost = 0
                total_joint2 = int(total_joint2) + int(each_joint2.total_cost)

            del total_joint_cost_list[d_index]
            total_joint_cost_list.insert(d_index, int(total_joint2))
        else:
            created_joint_list.insert(counter, each_joint2.created.strftime('%d, %b %Y'))
            try:
                total_joint_cost_list.insert(counter, int(each_joint2.total_cost))
            except:
                each_joint2.total_cost = 0
                total_joint_cost_list.insert(counter, int(each_joint2.total_cost))

    return render(request, 'anticipate/qwikadmin_sales_graph.html',  {'created_list': created_list,
                                                                        'created_user_list': created_user_list,
                                                                        'created_joint_list': created_joint_list,
                                                                        'static_total_cost2_list': static_total_cost2_list,
                                                                        'total_cost_list': total_cost_list, 'total_joint_cost_list': total_joint_cost_list})

@login_required
@permission_required('users.view_admin')
def showQwikAdminAntiCredits(request):
    context = {}
    filtered_antiorders = AntiOrderFilterCredits(
        request.GET,
        queryset = AntiOrder.objects.all()
    )
    context['filtered_antiorders'] = filtered_antiorders
    paginated_filtered_antiorders = Paginator(filtered_antiorders.qs, 10)
    page_number = request.GET.get('page')
    antiorders_page_obj = paginated_filtered_antiorders.get_page(page_number)
    context['antiorders_page_obj'] = antiorders_page_obj
    total_antiorders = filtered_antiorders.qs.count()
    context['total_antiorders'] = total_antiorders

    try:
        anti_balance = AntiOrder.objects.all().aggregate(Sum('balance'))['balance__sum']
    except:
        anti_balance = 0
    anti_balances = round(anti_balance,2)

    context['anti_balances'] = anti_balances

    return render(request, 'anticipate/qwikadmin_anti_credits.html', context=context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminAntiPayments(request):
    context = {}
    filtered_antiorders = AntiOrderFilterPayments(
        request.GET,
        queryset = AntiOrder.objects.all()
    )
    context['filtered_antiorders'] = filtered_antiorders
    paginated_filtered_antiorders = Paginator(filtered_antiorders.qs, 10)
    page_number = request.GET.get('page')
    antiorders_page_obj = paginated_filtered_antiorders.get_page(page_number)
    context['antiorders_page_obj'] = antiorders_page_obj
    total_antiorders = filtered_antiorders.qs.count()
    context['total_antiorders'] = total_antiorders

    return render(request, 'anticipate/qwikadmin_anti_payments.html', context=context)

@login_required
@permission_required('users.view_partner')
def updateQwikPartnerAntiOrders(request, id):
    order = AntiOrder.objects.get(id=id)
    form = AntiOrderFormPar(instance=order)
    if request.method=='POST':
        form = AntiOrderFormPar(request.POST, instance=order)
        if form.is_valid():
            # user = form.cleaned_data.get('user')
            payment2 = form.cleaned_data.get('payment2')
            form.save(commit=False).stage = "2nd"

            form.save()

            reg3 = AntiOrder.objects.get(id=id)
            try:
                reg3.payment_total = reg3.payment_total + payment2
            except:
                reg3.payment_total = 0 + payment2
            # reg3.payment_total = reg3.payment_total + payment2
            reg3.balance = reg3.static_total_cost2 - reg3.payment_total
            reg3.save()

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
            payment3 = form.cleaned_data.get('payment3')
            form.save(commit=False).stage = "3rd"
            form.save()
            reg3 = AntiOrder.objects.get(id=id)
            reg3.payment_total = reg3.payment_total + payment3
            reg3.balance = reg3.static_total_cost2 - reg3.payment_total
            reg3.save()
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

@login_required
def showAntiInvoiceUnPaid(request, pk, **kwargs):
    order = AntiOrder.objects.get(id=pk)
    # order_items = OrderItem.objects.filter(order__id=pk)
    context = {'order': order}#, 'order_items': order_items}
    return render(request, 'anticipate/anti_invoice_unpaid.html', context)

@login_required
@permission_required('users.view_admin')
def showQwikAdminAntiSales(request):
    context = {}
    filtered_antiorders = AntiOrderFilterSales(
        request.GET,
        queryset = AntiOrder.objects.all()
    )
    context['filtered_antiorders'] = filtered_antiorders
    paginated_filtered_antiorders = Paginator(filtered_antiorders.qs, 10)
    page_number = request.GET.get('page')
    antiorders_page_obj = paginated_filtered_antiorders.get_page(page_number)
    context['antiorders_page_obj'] = antiorders_page_obj
    total_antiorders = filtered_antiorders.qs.count()
    context['total_antiorders'] = total_antiorders

    try:
        anti_sale1 = AntiOrder.objects.all().aggregate(Sum('static_total_cost'))['static_total_cost__sum']
    except:
        anti_sale1 = 0
    try:
        anti_sale2 = AntiOrder.objects.all().aggregate(Sum('static_total_cost2'))['static_total_cost2__sum']
    except:
        anti_sale2 = 0

    anti_sale = anti_sale1 + anti_sale2
    anti_sales = round(anti_sale,2)

    context['anti_sales'] = anti_sales

    return render(request, 'anticipate/qwikadmin_anti_sales.html', context=context)

def exportCSVAntis(request):
    antis = AntiOrder.objects.prefetch_related(
        'cylinder'
    )
    response = HttpResponse(content_type='text/csv')
    now = datetime.datetime.now().strftime('%A_%d_%b_%Y')
    response['Content-Disposition'] = 'attachment; filename=Anticipatory ' + str(now) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Customer ID', 'outlet', 'Product Type (New)', 'Price (Old)', 'Price (New)', 'Total Cost (Old)', 'Total Cost (New)', 'Payment Choice', 'Transaction Status', 'Cylinder Alloted'])

    for each in antis:
        writer.writerow(
            [each.created.strftime('%A, %d, %b %Y'), each.user.username, each.outlet, ', '.join(c.category.type for c in each.cylinder.all()), each.static_price, ', '.join(str(c.category.price) for c in each.cylinder.all()), each.static_total_cost, each.static_total_cost2, each.payment_choice, each.transaction, ', '.join(c.product_Id for c in each.cylinder.all())]
        )
    return response

def exportCSVCredits(request):
    antis = AntiOrder.objects.prefetch_related(
        'cylinder'
    )
    response = HttpResponse(content_type='text/csv')
    now = datetime.datetime.now().strftime('%A_%d_%b_%Y')
    response['Content-Disposition'] = 'attachment; filename=Credit Sales ' + str(now) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Customer ID', 'outlet', 'Total Amount (Old)', 'Total Amount (New)', 'Payment Choice', '1st Payment/Date', '2nd Payment/Date', '3rd Payment/Date', 'Balance', 'Remark'])

    for each in antis:
        writer.writerow(
            [each.created.strftime('%A, %d, %b %Y'), each.user.username, each.outlet, each.static_total_cost, each.static_total_cost2, each.payment_choice, str(each.payment1)+"/"+str(each.payment1_date), str(each.payment2)+"/"+str(each.payment2_date), str(each.payment3)+"/"+str(each.payment3_date), each.balance, each.transaction]
        )
    return response

def exportCSVPayments(request):
    antis = AntiOrder.objects.prefetch_related(
        'cylinder'
    )
    response = HttpResponse(content_type='text/csv')
    now = datetime.datetime.now().strftime('%A_%d_%b_%Y')
    response['Content-Disposition'] = 'attachment; filename=Payments ' + str(now) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Customer ID', 'outlet', 'Amount', 'Payment Option', 'Payment Stage'])

    for each in antis:
        writer.writerow(
            [each.created.strftime('%A, %d, %b %Y'), each.user.username, each.outlet, each.payment_total, each.payment_choice, each.stage]
        )
    return response



# def exportPDF(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'inine; attachment; filename=Report' + str(datetime.datetime.now()) + '.pdf'
#     response['Content-Transfer-Encoding'] = 'binary'
#     anti_orders = AntiOrder.objects.all()
#
#     html_string = render_to_string('anticipate/pdf-output.html', {'antiorders_page_obj': 'anti_orders'})
#     html = HTML(string=html_string)
#     result = html.write_pdf()
#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush()
#         output = open(output.name, 'rb')
#         response.write(output.read())
#     return response
