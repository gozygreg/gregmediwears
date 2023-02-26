from django.contrib import admin
from django import forms
from .models import ShippingAddress, Order, OrderItem


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address1', 'address2', 'town_or_city', 'postcode']
        exclude = ['user',]


class ShippingAddressAdmin(admin.ModelAdmin):
    form = ShippingForm


class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('price',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdminInline,)

    readonly_fields = ('order_number', 'date_ordered', 'amount_paid')

    fields = ('user', 'order_number', 'full_name', 'date_ordered', 'email',
              'shipping_address', 'amount_paid')

    list_display = ('order_number', 'date_ordered', 'full_name', 'amount_paid')

    ordering = ('-date_ordered',)


admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
