from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# for pdf
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
# from weasyprint import HTML

# for mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# models from database
from acc_app.models import UserAccount, MerchantAccount, Message

# Create your views here.


@login_required(login_url='partner-login')
def admin_dashboard(request):

    return render(request, 'dashboard/admin/index.html')


@login_required(login_url='partner-login')
def admin_chat_list(request):
    context = {
        'merchant': UserAccount.objects.filter(is_staff)
    }
    return render(request, 'dashboard/admin/chat_table.html', context)


@login_required(login_url='partner-login')
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


@login_required(login_url='partner-login')
def admin_text_all(request):
    if request.method == "POST":
        message = request.POST['message']
        merchant_list = UserAccount.objects.filter(is_merchant)
        for merchant in merchant_list:
            Message.objects.create(sender=request.user,
                                   receiver=merchant, message=message)

    return render(request, 'dashboard/admin/notification.html')


@login_required(login_url='partner-login')
def admin_merchant_approval(request):

    context = {}
    sel_user = UserAccount.objects.filter(
        is_active=False, is_staff=False, is_superuser=False, is_merchant=False)

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
            sel.is_staff = False
            sel.is_superuser = False
            sel.is_merchant = True
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
                response['Content-Disposition'] = filename = str(
                    merchant_email + '.pdf')
                return response

    return render(request, 'dashboard/admin/new_merchant.html', context)
