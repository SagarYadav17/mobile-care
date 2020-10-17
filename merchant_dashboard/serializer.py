from rest_framework import serializers

from merchant_dashboard.models import Product

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'brand', 'name', 'price', 'warrenty', 'seller', 'description', 'available')