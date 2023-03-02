from decimal import Decimal
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import ShippingAddress, Order, OrderLineItem
from store.models import Product
from .forms import ShippingForm
from bag.bag import Bag
import stripe


def checkout(request):
    bag = Bag(request)
    shipping_form = ShippingForm()

    if request.method == 'POST':
        # Handle shipping address form submission
        shipping_form = ShippingForm(request.POST)
        if shipping_form.is_valid():
            shipping_address = shipping_form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            request.session['shipping_address'] = shipping_address.id
            return redirect(reverse('checkout_success'))

        # Handle payment form submission
        bag = request.session.get('bag', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        shipping_form = ShippingForm(form_data)
        if shipping_form.is_valid():
            shipping_form.save()

            # Iterate through bag items to create line item
            bag.__init__(self)
            return redirect(reverse('checckout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form.')

    # If no form submission, check bag contents
    else:
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('store'))

        # Create PaymentIntent
        order_total = bag.get_total()
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY
        stripe.api_key = settings.STRIPE_SECRET_KEY
        if not stripe_public_key:
            messages.warning(request, 'Your stripe public key is missing!')
            return redirect(reverse('store'))

        intent = stripe.PaymentIntent.create(
            amount=int(order_total * 100),
            currency='usd'
        )

    context = {
        'shipping_form': shipping_form,
        'bag': bag,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context=context)













def checkout_success(request):
    return render(request, 'checkout/checkout-success.html')


def checkout_failed(request):
    return render(request, 'checkout/checkout-failed.html')



