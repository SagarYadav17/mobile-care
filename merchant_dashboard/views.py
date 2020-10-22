from django.shortcuts import render, redirect
from acc_app.models import UserAccount, MerchantAccount

from django.contrib.auth.decorators import login_required

from rest_framework import viewsets

from merchant_app.models import Product
from merchant_app.serializer import ProductSerializer

from merchant_app.forms import ProductForm


# Create your views here.
class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer


@login_required(login_url='partner-login')
def merchant_dashboard(request):

    return render(request, 'dashboard/merchant/dashboard.html')


@login_required(login_url='partner-login')
def change_merchant_details(request):
    if request.method == 'POST':
        new_username = request.POST['username']

        update_status = UserAccount.objects.get(email=request.user)
        update_status.username = new_username
        update_status.save()

    return render(request, 'dashboard/merchant/form-advance.html')


@login_required(login_url='partner-login')
def merchant_components(request):

    return render(request, 'dashboard/merchant/component.html')


@login_required(login_url='partner-login')
def merchant_gallery(request):

    return render(request, 'dashboard/merchant/gallery.html')


@login_required(login_url='partner-login')
def merchant_invoice(request):

    return render(request, 'dashboard/merchant/invoice.html')


@login_required(login_url='partner-login')
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


@login_required(login_url='partner-login')
def merchant_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('merchant-product')

        else:
            print('Adding product failed from {}'.format(request.user.id))

    return render(request, 'dashboard/merchant/product.html', {'form': ProductForm})
