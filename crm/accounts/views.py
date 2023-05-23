from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Min, Max, Count
from .models import *
from .forms import OrderForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
# Create your views here.
def homeview(request):
    customer_qs = Customer.objects.all()
    order_qs = Order.objects.all()  
    cust_count = customer_qs.count()
    order_count = order_qs.count()
    delivered_count = order_qs.filter(status='Delivered').count()
    pending_count = order_qs.filter(status='Pending').count()
    context = {"customers":customer_qs, "orders":order_qs, "cust_count":cust_count, "order_count":order_count, "delivered_count":delivered_count, "pending_count":pending_count}
    return render(request,'accounts/dashboard.html', context)

def productview(request):
    product_qs = Product.objects.all()
    context = {'products':product_qs}
    return render(request,'accounts/products.html',context)

def customerview(request, id):
    context = {}
    order_filter = OrderFilter()
    if id:
        cust = Customer.objects.get(id=id)
        orders = cust.order_set.all()
        context = {"customer":cust, "orders":orders, "total_orders":orders.count(),"order_filter":order_filter }
    return render(request,'accounts/customer.html',context)

def create_order_view(request, id):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=3)
    cust = Customer.objects.get(id=id)
    # form = OrderForm(initial={'customer':cust})
    formset = OrderFormSet(queryset=Order.objects.none(),instance=cust)
    context = {'formset':formset }
    template = 'accounts/order_form.html'
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=cust)
        if formset.is_valid():
            formset.save()
            return redirect('/accounts/')
    return render(request,template,context)

def update_order_view(request, id):
    ord_obj = Order.objects.get(id=id)
    form = OrderForm(instance=ord_obj)
    if request.method == 'POST':
        data = request.POST
        form = OrderForm(data = data, instance=ord_obj)
        if form.is_valid():
            form.save()
            return redirect('/accounts/')
    context = {'form':form }
    template = 'accounts/order_form.html'
    return render(request,template,context)

def delete_order_view(request,id):
    o = Order.objects.get(id=id)
    if request.method=='POST':
        o.delete()
        return redirect('/accounts/')
    return render(request, 'accounts/delete.html', context={'item':o.product.name})

# class Order():
#     if request.method == 'GET':
