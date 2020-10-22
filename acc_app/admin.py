from django.contrib import admin

from acc_app.models import UserAccount, MerchantAccount, ShippingAddress


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    ordering = ['username']
    search_fields = ['email']
    list_filter = ['is_active', 'is_superuser', 'is_merchant']


class MerchantAccountAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'shop_name']
    ordering = ['full_name']


admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(MerchantAccount, MerchantAccountAdmin)
