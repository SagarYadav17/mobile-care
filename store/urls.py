from django.urls import path

from store import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.userLogin, name='login'),
    path('register/', views.register, name='register'),
]
