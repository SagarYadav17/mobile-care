from rest_framework import serializers

from merchant_app.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'brand', 'name', 'price', 'warrenty', 'seller', 'description', 'available')