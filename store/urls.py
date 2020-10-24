from django.urls import path

from store import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.userLogin, name='login'),
    path('register/', views.register, name='register'),
    path('explore/', views.products_list, name='explore'),
    path('product-detail/<int:product_id>',
         views.product_detail, name='product-detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name="update_item"),
    path('account/', views.account, name='account'),
    path('search/', views.search_result, name='search')
]
