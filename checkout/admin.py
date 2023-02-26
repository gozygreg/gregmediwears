from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem


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


class ShippingAddressAdmin(admin.ModelAdmin):
    pass


admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
