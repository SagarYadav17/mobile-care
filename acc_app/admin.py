from django.contrib import admin

from acc_app.models import UserAccount, MerchantAccount
# Register your models here.

class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    ordering = ['username']
    search_fields = ['email']
    list_filter = ['is_active', 'is_admin', 'is_staff']

class MerchantAccountAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'shop_name']
    ordering = ['full_name']

admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(MerchantAccount, MerchantAccountAdmin)