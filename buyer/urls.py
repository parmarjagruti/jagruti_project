from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('client/', client, name='client'),
    path('contact/', contact, name='contact'),
    path('products/', products, name='products'),
    path('add_row/', add_row, name='add_row'),
    path('register/', register, name='register'),
    path('otp/', otp, name='otp'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('cart/', cart, name = 'cart'),
    path('add_to_cart/<int:pk>', add_to_cart, name='add_to_cart'),
    path('remove_product/<int:pk>', remove_product,name='remove_product'),
    path('cart/paymenthandler/', paymenthandler, name='paymenthandler'),
]