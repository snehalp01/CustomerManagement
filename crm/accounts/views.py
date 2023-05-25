from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Min, Max, Count
from .models import *
from .forms import OrderForm, CustomUserCreationForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def loginView(request):
    if request.user.is_authenticated: return redirect('home')
    if request.method == 'POST':
        un = request.POST.get('username')
        pas = request.POST.get('password')
        user = authenticate(request, username=un,password=pas)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "username or password is incorrect")
    context = {}
    return render(request,'accounts/login.html')

def logoutview(request):
    logout(request)
    return redirect('loginview')

def registerView(request):
    if request.user.is_authenticated: return redirect('home')
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            usernm = form.cleaned_data.get('username')
            messages.success(request, 'account created successfully for '+usernm)
            return redirect("loginview")
    context = {"form":form}
    return render(request,'accounts/register.html', context)

@login_required(login_url = 'login/')
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

@login_required(login_url = 'login/')
def customerview(request, id):
    context = {}
    if id:
        cust = Customer.objects.get(id=id)
        orders = cust.order_set.all()
        orders_count = orders.count()
        order_filter = OrderFilter(request.GET, queryset=orders)
        orders = order_filter.qs
        context = {"customer":cust, "orders":orders, "total_orders":orders_count,"order_filter":order_filter }
    return render(request,'accounts/customer.html',context)

@login_required(login_url = 'login/')
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

@login_required(login_url = 'login/')
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

@login_required(login_url = 'login/')
def delete_order_view(request,id):
    o = Order.objects.get(id=id)
    if request.method=='POST':
        o.delete()
        return redirect('/accounts/')
    return render(request, 'accounts/delete.html', context={'item':o.product.name})
