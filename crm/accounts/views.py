from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def homeview(request):
    return render(request,template_name='accounts/dashboard.html')

def productview(request):
    return render(request,'accounts/products.html')

def customerview(request):
    return render(request,'accounts/customer.html')