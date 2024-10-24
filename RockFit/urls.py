from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fitness.urls')),  # Home view and app URL patterns
     path('cart/', include('cart.urls', namespace='cart')),  # Include the cart URLs with a namespace
]
