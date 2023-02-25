from django.urls import path
from . import views


urlpatterns = [
    path('checkout-success', views.checkout_success, name='checkout-success'),
    path('checkout-failed', views.checkout_failed, name='checkout-failed'),

]