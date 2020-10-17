from django.urls import path
from acc_app import views

urlpatterns = [
    path('join-us', views.partner_home, name='partner-home'),
    path('partner-login/', views.login_user, name='partner-login'),
    path('logout-user/', views.logout_user, name='logout-user'),
    path('merchant-register-form/', views.merchant_form,
         name='merchant-register-form'),
]
