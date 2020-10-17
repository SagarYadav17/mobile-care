from django.contrib import admin
from merchant_dashboard.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'seller', 'price']
    list_filter = ['available']
    ordering = ['name']

admin.site.register(Product, ProductAdmin)
