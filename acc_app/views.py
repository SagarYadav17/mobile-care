from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from acc_app.models import UserAccount, MerchantAccount

from django.contrib import messages

from django.db import IntegrityError
# Create your views here.


def register_user(request):
    if request.method == "POST":
        user_name = request.POST['username']
        e_mail = request.POST['email']
        pass_word = request.POST['password']

        User = get_user_model()
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
            return redirect('login-user')

        except IntegrityError as e:
            if str(e) == 'UNIQUE constraint failed: acc_app_useraccount.username':
                messages.info(request, 'username already taken')
            if str(e) == 'UNIQUE constraint failed: acc_app_useraccount.email':
                messages.info(request, 'email already taken')
            else:
                messages.info(request, 'something went wrong')

    return render(request, "acc_app/register.html")


def login_user(request):
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

    return render(request, 'acc_app/login.html')


def logout_user(request):
    logout(request)
    return redirect('login-user')


def home(request):
    if request.method == "POST":
        e_mail = request.POST['email']

        user = UserAccount.objects.filter(email=e_mail)
        if user:
            template = render_to_string(
                'mail/merchant_form_mail.html')

            email = EmailMessage(
                'Welcome to Mobile Care',
                template,
                settings.EMAIL_HOST_USER,
                [e_mail],
            )
            email.fail_silently = False
            email.send()
            return redirect('home')

    return render(request, 'index.html')


def soon(request):
    return render(request, 'progress.html')


def merchant_form(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        shopname = request.POST['shopname']
        email = request.POST['email']
        phone_number = request.POST['mb']
        phone_number1 = request.POST['mb1']
        aadhar = request.POST['adhar']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['zip']
        date = request.POST['dd']
        shopIMG = request.POST['image']
        shop_type = request.POST['shop-type']
        gst = request.POST['gst']
        services = request.POST['services']
        price = request.POST['price']

        new_merchant = MerchantAccount.objects.create(
            email=UserAccount.objects.get(email=email),
            full_name=fullname,
            shop_name=shopname,
            phone_num=phone_number,
            phone_num2=phone_number1,
            aadhar=aadhar,
            address=address,
            city=city.lower(),
            state=state.lower(),
            pincode=pincode,
            shop_established_date=date,
            shop_img=shopIMG,
            shop_type=shop_type,
            gst_num=gst,
            available_services=services,
            average_price=price
        )

        update_status = UserAccount.objects.get(email=email)
        update_status.is_active = False
        update_status.save()

        template = render_to_string(
            'mail/merchant_conformed.html', {'email': email})

        email = EmailMessage(
            'Welcome to Mobile Care',
            template,
            settings.EMAIL_HOST_USER,
            [email],
        )
        email.fail_silently = False
        email.send()
        
        return redirect('home')

    return render(request, 'acc_app/merchant_register_form.html')


@login_required(login_url='login-user')
def admin_dashboard(request):
    context = {}
    sel_user = UserAccount.objects.filter(
        is_active=False, is_staff=False, is_superuser=False)

    context['sel'] = sel_user

    if request.method == "POST":
        if "approve" in request.POST:
            sel_id = request.POST['id']
            sel = UserAccount.objects.get(id=sel_id)
            template = render_to_string(
                'mail/merchant_conformed.html', {'email': sel.email})

            email = EmailMessage(
                'Welcome to Mobile Care',
                template,
                settings.EMAIL_HOST_USER,
                [sel.email],
            )
            email.fail_silently = False
            email.send()

            sel.is_active = True
            sel.is_staff = True
            sel.save()

    return render(request, "dashboard/admin/admin.html", context)


@login_required(login_url='login-user')
def merchant_dashboard(request):
    merchant = MerchantAccount.objects.get(email=request.user)
    context = {'username': merchant.full_name}

    return render(request, 'dashboard/merchant/dashboard.html', context)


@login_required(login_url='login-user')
def change_merchant_details(request):
    merchant = MerchantAccount.objects.get(email=request.user)
    if request.method == 'POST':
        new_username = request.POST['username']
        update_status = UserAccount.objects.get(email=request.user)
        update_status.username = new_username
        update_status.save()

    return render(request, 'dashboard/merchant/form-advance.html')
