from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('acc_app.urls')),              # For acc_app
    path('', include('admin_dashboard.urls')),      # For admin_dashboard
    path('', include('merchant_dashboard.urls')),   # For merchant_dashboard
    path('', include('store.urls')),                # For store
    path('accounts/', include('allauth.urls')),     # For django-allauth
    path('', include('django.contrib.auth.urls')),  # For password reset
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
