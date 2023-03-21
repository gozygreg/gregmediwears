from django.http import HttpResponse
from .models import Order, OrderLineItem
from store.models import Product
import stripe
import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)

        print('INTENT: ', intent)

        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None
        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    shipping_address=shipping_details.address,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                print('IN TRY BLOCK')
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    shipping_address=shipping_details.address,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                print('ORDER: ', order)
                order_id = order.pk
                print('ORDER ID: ', order_id)
                print('BAG: ', bag)
                for item in bag:
                    print('IN FOR LOOP')
                    print('WH ITEM: ', item)
                    if item['qty'] >= 1:
                        OrderLineItem.objects.create(
                            order=order,
                            product=item['product'],
                            quantity=item['qty'],
                            lineitem_total=item['price'],
                        )
            except Exception as e:
                if order:
                    order.delete()
                print(e)
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)