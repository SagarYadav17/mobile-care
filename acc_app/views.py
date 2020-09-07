from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from acc_app.models import UserAccount

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
    return render(request, 'acc_app/merchant_register_form.html')
