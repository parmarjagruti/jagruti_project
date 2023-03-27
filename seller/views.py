from django.shortcuts import render, redirect
from random import randrange
from django.conf import settings
from .models import *
from buyer.models import *
from django.core.mail import send_mail

# Create your views here.

def seller_index(request):
    # condition is given becuse we want to verify that seller has
    #logged in or not
    try :
        s_obj = Seller.objects.get(email = request.session['seller_email'])
        return render(request, 'seller_index.html', {'seller_data': s_obj})
    except :
        return render(request, 'seller_index.html')

def seller_about(request):
    try :
        request.session['seller_email']
        return render(request, 'seller_about.html')
    except :
        return render(request, 'seller_about.html')

def seller_contact(request):
    try :
        request.session['seller_email']
        return render(request, 'seller_contact.html')
    except :
        return render(request, 'seller_contact.html')

def seller_blog(request):
    try :
        request.session['seller_email']
        return render(request, 'seller_blog.html')
    except :
        return render(request, 'seller_blog.html')

def seller_product(request):
    try :
        request.session['seller_email']
        return render(request, 'seller_product.html')
    except :
        return render(request, 'seller_product.html')

def seller_register(request):
    if request.method == 'GET':
        return render(request, 'seller_register.html')
    else :
        try :
            Buyer.objects.get(email = request.POST['email'])
            return render(request, 'seller_register.html',{'msg':'Email Is Already registered !!'})
        except :
            if request.POST['password'] == request.POST['repassword']:
                s = "Ecommerce Registration !!"
                global user_data
                user_data = [request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password']]
                global c_otp
                c_otp = randrange(1000,10000)
                m = f'Hello User !!\nYour OTP is {c_otp}'
                f = settings.EMAIL_HOST_USER
                r = [request.POST['email']]
                send_mail(s, m, f, r)
                return render(request, 'otp.html',{'msg': 'Check Your MailBox'})
            else :    
                return render(request, 'seller_register.html', {'msg': 'Both Password do not match !!'})

def seller_login(request):
    if request.method == 'GET':
        return render(request, 'seller_login.html')
    else:
        try :
            seller_obj = Seller.objects.get(email = request.POST['email'])
            if request.POST['password'] == seller_obj.password :
                request.session['seller_email'] = request.POST['email']
                return render(request, 'seller_index.html', {'seller_data' : seller_obj})
            else :
                return render(request, 'seller_login.html', {'msg': 'wrong password !!'})
        except :
            return render(request, 'seller_login.html', {'msg':'email is not registered'})


def seller_logout(request):
    del request.session['seller_email']
    return redirect('seller_login.html')


def seller_edit_profile(request):
    return render(request, 'seller_edit_profile.html')


def my_products(request):
    return render(request, 'my_products.html')

def add_product(request):
    seller_obj = Seller.objects.get(email = request.session['seller_email'])
    if request.method == 'GET':
        return render(request, 'add_product.html', {'seller_data':seller_obj})
    else:
        #ek product db ma add karishu
        Product.objects.create(
            product_name = request.POST['product_name'],
            des = request.POST['des'],
            price = request.POST['price'],
            product_stock = request.POST['product_stock'],
            pic = request.FILES['pic'],
            seller = seller_obj
        )
        return redirect('add_product')
    

def my_products(request):
    s_obj = Seller.objects.get(email = request.session['seller_email'])
    my_pros = Product.objects.filter(seller = s_obj )
    return render(request, 'my_products.html', {'seller_data': s_obj, 'my_all_product':my_pros})

        
def product_delete(request,pk):
    p_obj = Product.objects.get(id=pk)
    p_obj.delete()
    return redirect('my_products')


def product_edit(request, pk):
    p_obj = Product.objects.get(id = pk)
    if request.method == 'GET':
        seller_obj = Seller.objects.get(email = request.session['seller_email'])
        return render(request, 'edit_product.html', {'seller_data':seller_obj, 'product_data': p_obj})
    else:
        p_obj.product_name = request.POST['product_name']
        p_obj.des = request.POST['des']
        p_obj.price = request.POST['price']
        p_obj.product_stock = request.POST['product_stock']
        p_obj.pic = request.FILES['pic']
        p_obj.save()
        return redirect('my_product')

