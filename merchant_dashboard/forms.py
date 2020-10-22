from django import forms
from merchant_app.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('brand', 'name', 'image', 'price',
                  'warrenty', 'description', 'seller')
