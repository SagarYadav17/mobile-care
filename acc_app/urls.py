from django.urls import path

from acc_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register-user'),
    path('login/', views.login_user, name='login-user'),
    path('logout-user/', views.logout_user, name='logout-user'),
    path('merchant-register-form/', views.merchant_form, name='merchant-register-form'),
    path('confirm-merchant', views.merchant_form, name='confirm-merchant'),

    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('merchant-dashboard/', views.merchant_dashboard, name='merchant-dashboard'),

    path('merchant-dashboard/change-profile/', views.change_merchant_details, name='change-merchant-details'),

    path('work-in-progress/', views.soon, name='soon')
]
