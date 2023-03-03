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

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    stripe.api_key = stripe_secret_key

    intent = None

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')

        # All-in-one shipping address
        shipping_address = (address1 + "\n" + address2 + "\n" + city + "\n" + county + "\n" + country + "\n" +"\n" + postcode)

        # Shipping cart information
        bag = Bag(request)

        # Get the total price of item
        total_cost = bag.get_total()

        '''
        order variations
        1) Create order - Account users with + without shipping information
        2) Create order - Guest users without an account
        '''
        # 1) Create order - Account users with + without shipping information
        if request.user.is_authenticated:
            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address, order_total=total_cost, user=request.user)
            order_id = order.pk
            for item in bag:
                OrderLineItem.objects.create(order_id=order_id, product=item['product'], quantity=item['price'], user=request.user)

        # 2) Create order - Guest users  without an account
        else:
            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address, order_total=total_cost)
            order_id = order.pk
            for item in bag:
                OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'], price=item['price'])

        # Handle shipping address form submission
        shipping_form = ShippingForm(request.POST)
        if shipping_form.is_valid():
            shipping_address = shipping_form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            request.session['shipping_address'] = shipping_address.id
            return redirect(reverse('checkout_success'))

        # Handle payment form submission
        else:
            # Create PaymentIntent
            order_total = bag.get_total()
            stripe.api_key = stripe_secret_key

            if not stripe_public_key:
                messages.warning(request, 'Your stripe public key is missing!')
                return redirect(reverse('store'))

            intent = stripe.PaymentIntent.create(
                amount=int(order_total * 100),
                currency='usd'
            )

    # Check bag contents
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('store'))

    try:
        client_secret = intent.client_secret
    except AttributeError:
        client_secret = ''

    context = {
        'shipping_form': shipping_form,
        'bag': bag,
        'stripe_public_key': stripe_public_key,
        'client_secret': client_secret,
    }

    # users with accounts -- pre-fill the form
    if request.user.is_authenticated:
        try:
            # Authenticated users with shipping information
            shipping_address = ShippingAddress.objects.get(user=request.user.id)
            context['shipping'] = shipping_address
        except:
            # Authenticated users without shipping information
            pass

    return render(request, 'checkout/checkout.html', context=context)















def checkout_success(request):
    return render(request, 'checkout/checkout-success.html')


def checkout_failed(request):
    return render(request, 'checkout/checkout-failed.html')




