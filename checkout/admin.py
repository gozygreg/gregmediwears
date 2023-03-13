from django.contrib import admin
from django import forms
from .models import ShippingAddress, Order, OrderLineItem


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address1', 'address2', 'town_or_city', 'postcode']
        exclude = ['user',]


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address1', 'address2', 'town_or_city', 'postcode')


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderLineItemAdminInline]

    readonly_fields = ('order_number', 'date_ordered', 'order_total', 'grand_total', 'original_bag', 'stripe_pid')

    fields = ('user', 'order_number', 'full_name', 'date_ordered', 'email',
              'shipping_address', 'order_total', 'grand_total', 'original_bag', 'stripe_pid')

    list_display = ('order_number', 'date_ordered', 'full_name', 'order_total', 'grand_total')

    ordering = ('-date_ordered',)


admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)

