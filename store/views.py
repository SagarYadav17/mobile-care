from django.shortcuts import render, redirect

from merchant_dashboard.models import Product
from acc_app.models import UserAccount, MerchantAccount

from django.db import IntegrityError

from django.contrib.auth import login, authenticate

# for email
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


# for error handeling
from django.contrib import messages


def home(request):
    return render(request, 'store/index.html')


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
            login(request)
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
