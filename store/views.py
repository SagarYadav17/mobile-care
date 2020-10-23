from django.shortcuts import render, redirect

from merchant_dashboard.models import Product
from acc_app.models import UserAccount, MerchantAccount, ShippingAddress
from store.models import Order, OrderItem

from django.db import IntegrityError

from django.contrib.auth import login, authenticate

# for email
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


# for error handeling
from django.contrib import messages

from store import utils
from store.forms import AddressForm

import json
from django.http import JsonResponse

import random


def home(request):
    data = utils.cartData(request)
    order = data['order']
    context = {'order': order}
    return render(request, 'store/index.html', context)


def userLogin(request):
    if request.method == 'POST':
        e_mail = request.POST['username']
        pswd = request.POST['password']

        email_login = authenticate(email=e_mail, password=pswd)
        username_login = authenticate(username=e_mail, password=pswd)

        if email_login:
            login(request, email_login)
            return redirect('home')

        elif username_login:
            login(request, username_login)
            return redirect('home')

        else:
            messages.info(request, 'Your entered wrong credentials')

    return render(request, 'store/login.html')


def register(request):
    if request.method == "POST":
        user_name = request.POST['username']
        e_mail = request.POST['email']
        pass_word = request.POST['password']

        try:
            user = UserAccount.objects.create_activeuser(
                username=user_name, email=e_mail, password=pass_word)
            template = render_to_string(
                'mail/welcome_mail.html', {'email': e_mail})

            email = EmailMessage(
                'Welcome to Mobile Care',
                template,
                settings.EMAIL_HOST_USER,
                [e_mail],
            )
            email.fail_silently = False
            email.send()
            return redirect('store')

        except IntegrityError as e:
            if str(e) == 'UNIQUE constraint failed: acc_app_useraccount.username':
                messages.info(request, 'username already taken')
            if str(e) == 'UNIQUE constraint failed: acc_app_useraccount.email':
                messages.info(request, 'email already taken')
            else:
                messages.info(request, 'something went wrong')

    return render(request, 'store/register.html')


def cart(request):
    data = utils.cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}

    return render(request, 'store/cart.html', context)


def product_detail(request, product_id):
    product_detail = Product.objects.get(id=product_id)

    context = {
        'product': product_detail,
        'ratings': random.randint(1, 5)
    }

    return render(request, 'store/product-detail.html', context)


def checkout(request):
    return render(request, 'store/check-out.html')


def products_list(request):
    data = utils.cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products}

    return render(request, 'store/products-list.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def account(request):
    content = {}
    try:
        content['account_data'] = ShippingAddress.objects.get(
            customer=request.user.id)
    except:
        content['account_data'] = None

    content['form'] = AddressForm

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account')

    return render(request, 'store/account.html', content)
