from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fitness.urls')),  # Include fitness app URLs
    path('cart/', include('cart.urls', namespace='cart')),  # Include cart app URLs
    path('accounts/', include('allauth.urls')),  # Include allauth's URLs
]
