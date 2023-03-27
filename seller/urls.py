from .views import *
from django.urls import path


urlpatterns = [
    path('', seller_index, name='seller_index'),
    path('seller_index/', seller_index, name='seller_index'),
    path('seller_about/', seller_about, name='seller_about'),
    path('seller_contact/', seller_contact, name='seller_contact'),
    path('seller_blog/', seller_blog, name='seller_blog'),
    path('seller_product/', seller_product, name='seller_product'),
    path('seller_register/', seller_register, name='seller_register'),
    path('seller_login/', seller_login, name='seller_login'),
    path('seller_logout/', seller_logout, name='seller_logout'),
    path('seller_edit_profile/', seller_edit_profile, name='seller_edit_profile'),
    path('my_products/', my_products, name='my_products'),
    path('add_product/', add_product, name='add_product'),
    path('product_edit/<int:pk>', product_edit, name='product_edit'),
    path('my_product/', my_products, name='my_product'),
    path('product_delete/<int:pk>',product_delete, name='product_delete')
]



