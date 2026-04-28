from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Cart URLs
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.add_to_cart_api, name='add_to_cart'),
    path('cart/remove/', views.remove_from_cart_api, name='remove_from_cart'),
    path('cart/update/', views.update_cart_api, name='update_cart'),
    
    # Checkout URLs
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/process/', views.process_checkout, name='process_checkout'),
    
    # Payment URLs
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('payment/success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('payment/cancel/<int:order_id>/', views.payment_cancel, name='payment_cancel'),
    path('payment/notify/', views.payment_notify, name='payment_notify'),
]