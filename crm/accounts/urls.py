from django.urls import path
from .views import homeview,productview, productview, customerview

urlpatterns = [
    path('', homeview),
    path('product/', productview),
    path('customer/', customerview),
]