import razorpay
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from .models import *
from django.core.mail import send_mail
from random import randrange
from django.conf import settings
from seller.models import *
from django.views.decorators.csrf import csrf_exempt



# create your views here.

def index(request):
    print('#################################################3')
    all_pros = Product.objects.all()
    print('-------------------------------------------')
    print(all_pros)
    print('-------------------------------------------')

    try :
        buyer_row = Buyer.objects.get(email = request.session['email'])
        return render(request, 'index.html',{'user_data' : buyer_row, 'all_products' : all_pros})
    except :
        print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
        return render(request, 'index.html', {'all_products' : all_pros})

def about(request):
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    try :
        buyer_row = Buyer.objects.get(email = request.session['email'])
        return render(request, 'about.html',{'user_data': buyer_row})
    except :
        return render(request, 'about.html')

 
def client(request):
    try :
        buyer_row = Buyer.objects.get(email = request.session['email'])
        return render(request, 'client.html', {'user_data' : buyer_row})
    except :
        return render(request, 'client.html')

def contact(request):
    try :
        buyer_row = Buyer.objects.get(email = request.session['email'])
        return render(request, 'contact.html', {'user_data' : buyer_row})
    except :
        return render(request, 'contact.html')
    

def products(request):
    try :
        buyer_row = Buyer.objects.get(email = request.session['email'])
        return render(request, 'products.html', {'user_data' : buyer_row})
    except :
        return render(request, 'products.html')

def add_row(request):
    Buyer.objects.create(
        first_name = 'rinkal',
        last_name = 'patel',
        email = 'r@gmail.com',
        password = 'tops@123',
        address = 'goyandi, bilimora',
        mobile = '8735903870',
        gender = 'female'
    )
    return HttpResponse('row create thai gai')



def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else :
        try :
            Buyer.objects.get(email = request.POST['email'])
            return render(request, 'register.html',{'msg':'Email Is Already registered !!'})
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
                return render(request, 'register.html', {'msg': 'Both Password do not match !!'})


def otp(request):
    if int(c_otp) == int(request.POST['u_otp']):
        Buyer.objects.create(
            first_name = user_data[0],
            last_name = user_data[1],
            email = user_data[2],
            password = user_data[3]
        )
        return render(request, 'login.html', {'msg' : 'Account create successfuly !!'})
    else :
        return render(request, 'otp.html', {'msg' : 'Wrong OTP enter again !!'})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        try :
            buyer_row = Buyer.objects.get(email = request.POST['email'])
            if request.POST['password'] == buyer_row.password :
                request.session['email'] = request.POST['email']
                return redirect('index')
            else :
                return render(request, 'login.html', {'msg': 'wrong password !!'})
        except :
            return render(request, 'login.html', {'msg':'email is not registered'})


def logout(request) :
    del request.session['email']
    return redirect('index')


    
def add_to_cart(request, pk):
    p_obj = Product.objects.get(id = pk)
    try:
    # if(1):
        print('---------------------------------------')
        print(request.session['email'])
        b1 = Buyer.objects.get(email = request.session['email'])
        Cart.objects.create(
           product = p_obj,
            buyer = b1
        )
        return redirect('index')
    except:
    # else:
        return redirect('login')


def cart(request):
    if request.method == 'GET':
        # try:
        if(1):
            buyer_obj = Buyer.objects.get(email=request.session['email'])
            cart_list = Cart.objects.filter(buyer=buyer_obj)
            # print(cart_list[0].buyer.first_name)
            # print((cart_list[0]))
            # print((cart_list[1]))
            # print((cart_list[2]))
            # print((cart_list[3]))
            total_products = len(cart_list)
            global total_price
            total_price = 0
            for i in list(cart_list):
                # print(i.product.seller)
                print('-----------------------------------------------------')
                print(i.product.price)
                total_price = total_price + i.product.price

            # payment nu button jivit karva maate no code
            currency = 'INR'
            amount = float(total_price*8000)  # total_price is in dollar

            # Create a Razorpay Order
            razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                               currency=currency,
                                                               payment_capture='0'))

            # order id of newly created order.
            razorpay_order_id = razorpay_order['id']
            callback_url = 'paymenthandler/'

            # we need to pass these details to frontend.
            context = {}
            context['razorpay_order_id'] = razorpay_order_id
            context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
            context['razorpay_amount'] = amount
            context['currency'] = currency
            context['callback_url'] = callback_url
            context.update(
                {'cart_list': cart_list, 'total_price': amount/100, 'total_products': total_products})
            print(total_price)
            return render(request, 'cart.html', context=context)
        # except:
        else:
            return HttpResponse('error')
    else:
        return HttpResponse('this is post method part')


def remove_product(request, pk):
    c_delete = Cart.objects.get(id=pk)
    c_delete.delete()
    return redirect('cart')


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.

@csrf_exempt
def paymenthandler(request):

    # only accept POST request.
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = float(total_price*8000)  # Rs. 200
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    return render(request, 'paymentsuccess.html')
                except:

                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:

                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()