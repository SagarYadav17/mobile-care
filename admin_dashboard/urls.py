from django.urls import path
from admin_dashboard import views

urlpatterns = [
    # admin dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('admin-chat-list/', views.admin_chat_list, name='admin-chat-list'),
    path('admin-chat/<str:merchant_email>/',
         views.admin_chat, name='admin-chat'),
    path('admin-merchant-approval/', views.admin_merchant_approval,
         name='admin-merchant-approve'),
    path('admin-text-all-merchant/', views.admin_text_all,
         name='admin-text-all-merchant'),

]
