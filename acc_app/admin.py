from django.contrib import admin

from acc_app.models import UserAccount
# Register your models here.

class UserAccountAdmin(admin.ModelAdmin):
    search_fields = ['email']
    list_filter = ['is_active', 'is_admin', 'is_staff']

admin.site.register(UserAccount, UserAccountAdmin)
