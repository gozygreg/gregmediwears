from django.urls import path
from . import views
from .webhooks import webhook


urlpatterns = [
    path('checkout', views.checkout, name='checkout'),
    path('checkout-success/<order_number>', views.checkout_success, name='checkout-success'),
    path('checkout-failed', views.checkout_failed, name='checkout-failed'),
    path('wh/', webhook, name='webhook'),

]