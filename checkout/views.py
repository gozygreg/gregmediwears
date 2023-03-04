from decimal import Decimal
import stripe

from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404

from bag.bag import Bag
from checkout.forms import ShippingForm
from checkout.models import Order, OrderLineItem, ShippingAddress
from store.models import Product

stripe_public_key = settings.STRIPE_PUBLIC_KEY
stripe_secret_key = settings.STRIPE_SECRET_KEY
stripe.api_key = stripe_secret_key


def checkout(request):
    bag = Bag(request)
    shipping_form = ShippingForm()
    intent = None

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        town_or_city = request.POST.get('town_or_city')
        county = request.POST.get('county')
        postcode = request.POST.get('postcode')

        # All-in-one shipping address
        shipping_address = (
            f'{address1}\n{address2}\n{town_or_city}\n{county}\n{postcode}'
        )

        # Shipping cart information
        total_cost = bag.get_total()
        stripe_total = round(total_cost * 100)

        try:
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )

            order, created = Order.objects.get_or_create(
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                order_total=total_cost,
                user=request.user if request.user.is_authenticated else None
            )

            for item in bag:
                OrderLineItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['qty'],
                    price=item['price'],
                    user=request.user if request.user.is_authenticated else None
                )

            bag.clear_bag()
            messages.success(request, f'Your order has been processed! \
                Your order number is {order.order_number}. You will receive a confirmation email shortly.')
            return redirect(reverse('store'))

        except stripe.error.CardError as e:
            intent = None
            messages.error(request, f'Your card was declined: {e.error.message}')

    if intent is None:
        current_bag = bag
        total = current_bag.get_total()

        stripe_total = round(total * 100)
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

    context = {
        'shipping_form': shipping_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'bag': bag,
        'total': total,
    }

    return render(request, 'checkout/checkout.html', context)



def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
            email will be sent to {order.email}.')

    context = {'order': order}
    return render(request, 'checkout/checkout-success.html', context=context)


def checkout_failed(request):
    return render(request, 'checkout/checkout-failed.html')