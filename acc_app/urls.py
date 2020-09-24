from django.urls import path
from acc_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register-user'),
    path('login/', views.login_user, name='login-user'),
    path('logout-user/', views.logout_user, name='logout-user'),
    path('merchant-register-form/', views.merchant_form,
         name='merchant-register-form'),
    path('confirm-merchant/', views.merchant_form, name='confirm-merchant'),

    # admin dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('admin-chat-list/', views.admin_chat_list, name='admin-chat-list'),
    path('admin-chat/<str:merchant_email>/',
         views.admin_chat, name='admin-chat'),
    path('admin-merchant-approval/', views.admin_merchant_approval,
         name='admin-merchant-approve'),
         path('admin-text-all-merchant/', views.admin_text_all, name='admin-text-all-merchant'),


    # merchant dashboard
    path('merchant-dashboard/', views.merchant_dashboard,
         name='merchant-dashboard'),
    path('merchant-dashboard/change-profile/',
         views.change_merchant_details, name='change-merchant-details'),
    path('merchant-dashboard/components/',
         views.merchant_components, name='merchant-component'),
    path('merchant-dashboard/gallery/',
         views.merchant_gallery, name='merchant-gallery'),
    path('merchant-dashboard/invoice/',
         views.merchant_invoice, name='merchant-invoice'),
    path('merchant-dashboard/messages/',
         views.merchant_messages, name='merchant-message'),
    path('merchant-dashboard/products/',
         views.merchant_product, name='merchant-product'),


    path('work-in-progress', views.soon, name='soon')
]
