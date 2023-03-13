from django.http import HttpResponse
from .models import Order, OrderLineItem
from store.models import Product
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

        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None
        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name_iexact=shipping_details.name,
                    email_iexact=billing_details.email,
                    country_iexact=shipping_details.address.country,
                    postcode_iexact=shipping_details.address.postal_code,
                    town_or_city_iexact=shipping_details.address.city,
                    address1_iexact=shipping_details.address.line1,
                    address2_iexact=shipping_details.address.line2,
                    county_iexact=shipping_details.address.state,
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
                if request.user.is_authenticated:
                    order = Order.objects.create(
                        full_name=shipping_details.name,
                        email=billing_details.email,
                        country_=shipping_details.address.country,
                        postcode=shipping_details.address.postal_code,
                        town_or_city=shipping_details.address.city,
                        address1=shipping_details.address.line1,
                        address2=shipping_details.address.line2,
                        county=shipping_details.address.state,
                        user=request.user,
                        original_bag=bag,
                        stripe_pid=pid,
                    )
                    order_id = order.pk
                    for item in json.loads(bag):
                        if item['qty'] >= 1:
                            OrderLineItem.objects.create(
                                order=order,
                                product=item['product'],
                                quantity=item['qty'],
                                lineitem_total=item['price'],
                                user=request.user
                            )
                # 2) Create order - Guest users  without an account
                else:
                    order = Order.objects.create(
                        full_name=shipping_details.name,
                        email=billing_details.email,
                        country_=shipping_details.address.country,
                        postcode=shipping_details.address.postal_code,
                        town_or_city=shipping_details.address.city,
                        address1=shipping_details.address.line1,
                        address2=shipping_details.address.line2,
                        county=shipping_details.address.state,
                        user=request.user,
                        original_bag=bag,
                        stripe_pid=pid,
                        )
                    order_id = order.pk
                    for item in bag:
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