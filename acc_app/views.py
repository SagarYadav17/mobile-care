from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

# for email
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# models from database
from acc_app.models import UserAccount, MerchantAccount

# for error handeling
from django.contrib import messages


# Create your views here.

def login_user(request):
    if request.method == 'POST':

        e_mail = request.POST['username']
        pswd = request.POST['password']

        email_login = authenticate(email=e_mail, password=pswd)
        username_login = authenticate(username=e_mail, password=pswd)

        if email_login:
            login(request, email_login)
            if request.user.is_merchant:
                return redirect('merchant-dashboard')
            elif request.user.is_superuser:
                return redirect('admin-dashboard')
            else:
                messages.info(request, 'Not merchant')

        elif username_login:
            login(request, username_login)
            if request.user.is_merchant:
                return redirect('merchant-dashboard')
            elif request.user.is_superuser:
                return redirect('admin-dashboard')
            else:
                messages.info(request, 'Not merchant')

        else:
            messages.info(request, 'Your entered wrong credentials')

    return render(request, 'acc_app/login.html')


def logout_user(request):
    logout(request)
    return redirect('home')


def partner_home(request):
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
        update_status.is_superuser = True
        update_status.save()

        template = render_to_string(
            'mail/merchant_in_review.html', {'email': email})

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
