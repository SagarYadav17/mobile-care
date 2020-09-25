from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from acc_app.models import UserAccount, MerchantAccount, Message

from django.contrib import messages

from django.db import IntegrityError

from weasyprint import HTML

# Create your views here.


def register_user(request):
    if request.method == "POST":
        user_name = request.POST['username']
        e_mail = request.POST['email']
        pass_word = request.POST['password']

        try:
            UserAccount.objects.create_activeuser(
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
            return redirect('home')

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
            return redirect('merchant-dashboard')

        elif username_login:
            login(request, username_login)
            return redirect('merchant-dashboard')

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
        about = request.POST['about-shop']

        MerchantAccount.objects.create(
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
            about_shop=about,
        )

        update_status = UserAccount.objects.get(email=email)
        update_status.is_active = False
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

# Admin section


@login_required(login_url='login-user')
def admin_dashboard(request):

    return render(request, "dashboard/admin/index.html")


@login_required(login_url='login-user')
def admin_chat_list(request):
    context = {
        'merchant': UserAccount.objects.filter(is_superuser=False and is_staff)
    }
    return render(request, 'dashboard/admin/chat_table.html', context)


@login_required(login_url='login-user')
def admin_chat(request, merchant_email):
    merchant_data = UserAccount.objects.get(email=merchant_email)

    all_messages = {
        'email': merchant_email,
        'receiver': UserAccount.objects.get(email=merchant_data),
        'messages': Message.objects.filter(sender=merchant_data, receiver=request.user) |
        Message.objects.filter(sender=request.user, receiver=merchant_data)
    }

    if request.method == 'POST':
        msg = request.POST['message']
        Message.objects.create(sender=request.user,
                               receiver=merchant_data, message=msg)
        return redirect('admin-chat', merchant_data)

    return render(request, 'dashboard/admin/chat.html', all_messages)


@login_required(login_url='login-user')
def admin_text_all(request):
    if request.method == "POST":
        message = request.POST['message']
        merchant_list = UserAccount.objects.filter(
            is_superuser=False and is_staff)
        for merchant in merchant_list:
            Message.objects.create(sender=request.user,
                                   receiver=merchant, message=message)

    return render(request, 'dashboard/admin/notification.html')


@login_required(login_url='login-user')
def admin_merchant_approval(request):

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

        if "pdf" in request.POST:
            sel_id = request.POST['id']
            merchant_id = UserAccount.objects.get(id=sel_id)
            merchant_email = merchant_id.email
            merchant_data = MerchantAccount.objects.get(
                email__email__contains=merchant_email)

            template = render_to_string(
                'export-merchant-data.html', {'merchant_data': merchant_data})

            file_date = HTML(string=template)
            file_date.write_pdf(target='/tmp/' + merchant_email + '.pdf')

            fs = FileSystemStorage('/tmp')
            with fs.open(merchant_email + '.pdf') as pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = str(
                    merchant_email + '.pdf')
                return response

    return render(request, 'dashboard/admin/new_merchant.html', context)


# Merchant Section


@login_required(login_url='login-user')
def merchant_dashboard(request):

    return render(request, 'dashboard/merchant/dashboard.html')


@login_required(login_url='login-user')
def change_merchant_details(request):
    if request.method == 'POST':
        new_username = request.POST['username']

        update_status = UserAccount.objects.get(email=request.user)
        update_status.username = new_username
        update_status.save()

    return render(request, 'dashboard/merchant/form-advance.html')


@login_required(login_url='login-user')
def merchant_components(request):

    return render(request, 'dashboard/merchant/component.html')


@login_required(login_url='login-user')
def merchant_gallery(request):

    return render(request, 'dashboard/merchant/gallery.html')


@login_required(login_url='login-user')
def merchant_invoice(request):

    return render(request, 'dashboard/merchant/invoice.html')


@login_required(login_url='login-user')
def merchant_messages(request):

    admin = UserAccount.objects.get(is_superuser=True)

    all_messages = {
        'receiver': UserAccount.objects.get(email=admin),
        'messages': Message.objects.filter(sender=admin, receiver=request.user) |
        Message.objects.filter(sender=request.user, receiver=admin)
    }

    if request.method == 'POST':
        msg = request.POST['message']
        Message.objects.create(sender=request.user,
                               receiver=admin, message=msg)
        return redirect('merchant-message')

    return render(request, 'dashboard/merchant/message-task.html', all_messages)


@login_required(login_url='login-user')
def merchant_product(request):

    return render(request, 'dashboard/merchant/product.html')
