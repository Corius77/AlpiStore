from django.urls import path, include

from . import views

app_name = 'product'

urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
    path('cart/', views.cart, name='cart'),
    path('list/', views.list, name='list'),
    path('details/', views.details, name='details/'),
    path('checkout/', views.checkout, name='checkout'),
    path('paypal/', include("paypal.standard.ipn.urls")),
    path('paypal_success/', views.paypal_success, name='paypal_success'),
    path('orders/', views.payed_orders, name='orders')
]