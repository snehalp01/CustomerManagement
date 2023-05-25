from django.urls import path
from .views import homeview,productview, productview, customerview, create_order_view, update_order_view,delete_order_view, loginView, registerView, logoutview

urlpatterns = [
    path('', homeview, name="home"),
    path('login/',loginView, name='loginview' ),
    path('logout/',logoutview, name='logoutview'),
    path('register/',registerView, name='registerview' ),
    path('product/', productview, name="products"),
    path('customer/<str:id>/', customerview, name="customer"),
    path('order-form/<str:id>', create_order_view, name="placeOrder"),
    path('order/<str:id>', update_order_view,name="updateOrder"),
    path('delete_order_view/<str:id>', delete_order_view, name="deleteorder")
]