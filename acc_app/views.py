from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from acc_app.models import UserAccount

# Create your views here.


def register_user(request):
    if request.method == "POST":
        e_mail = request.POST['email']
        password = request.POST['password']
        User = get_user_model()
        user = UserAccount.objects.create_activeuser(e_mail, password)

        user.save()
        template = render_to_string('welcome_mail.html', {'email': e_mail})
        email = EmailMessage(
            'Welcome to Mobile Care',
            template,
            settings.EMAIL_HOST_USER,
            [e_mail],
        )
        email.fail_silently = False
        email.send()
        print(e_mail)
        return redirect('login-user')

    return render(request, "acc_app/register.html")


def login_user(request):
    if request.method == 'POST':
        e_mail = request.POST['email']
        pswd = request.POST['password']
        user = authenticate(email=e_mail, password=pswd)
        if user:
            login(request, user)

            if user.is_active:
                return redirect('home')

    return render(request, 'acc_app/login.html')


def merchant_registeration(request):
    return render(request, 'acc_app/merchant_form.html')


def logout_user(request):
    logout(request)
    return redirect('login-user')


def home(request):
    return render(request, 'index.html')


def soon(request):
    return render(request, 'progress.html')
