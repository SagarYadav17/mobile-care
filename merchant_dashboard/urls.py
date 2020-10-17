from django.urls import path, include
from merchant_dashboard import views

from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=True)
router.register('product', views.ProductView)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),


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
]
