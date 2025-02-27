from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path('add/<int:item_id>/<str:item_type>/', views.add_to_cart, name='add_to_cart'),
    path('', views.view_cart, name='view_cart'),
    path('subscription/add_to_cart/<int:plan_id>/', views.add_subscription_to_cart, name='add_subscription_to_cart'),
    path('remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:cart_item_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/<int:order_id>/', views.checkout, name='checkout'),
    path('success/', views.payment_success, name='success'),
    path('cancel/', views.cancel_view, name='cancel'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('payment_failed/', views.payment_failed, name='payment_failed'),
   
]