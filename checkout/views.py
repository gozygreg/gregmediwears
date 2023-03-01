from decimal import Decimal
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import ShippingAddress, Order, OrderLineItem
from .forms import ShippingForm
from bag.bag import Bag
import stripe
import json


def checkout(request):
    bag = Bag(request)
    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            request.session['shipping_address'] = shipping_address.id
            return redirect(reverse('checkout_success'))
    else:
        form = ShippingForm()

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    stripe.api_key = settings.STRIPE_SECRET_KEY

    order_total = bag.get_total()
    intent = stripe.PaymentIntent.create(
        amount=int(order_total * 100),
        currency='usd'
    )

    if not stripe_public_key:
        messages.warning(request, 'Your stripe public key is missing!')
    context = {
        'form': form,
        'bag': bag,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context=context)







def checkout_success(request):
    return render(request, 'checkout/checkout-success.html')


def checkout_failed(request):
    return render(request, 'checkout/checkout-failed.html')