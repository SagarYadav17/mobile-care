from django import forms

from acc_app.models import ShippingAddress


class AddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ('__all__')
