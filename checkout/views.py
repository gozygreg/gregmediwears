from django.shortcuts import render
from .models import ShippingAddress


def checkout(request):
    # users with accounts -- pre-fill the form
    if request.user.is_authenticated:
        try:
            # Authenticated users with shipping information
            shipping_address = ShippingAddress.objects.get(user=request.user.id)
            context = {'shipping': shipping_address}
            return render(request, 'checkout/checkout.html', context=context)
        except:
            # Authenticated users without shipping information
            return render(request, 'checkout/checkout.html')
    else:
        # Guest user
        return render(request, 'checkout/checkout.html')



    return render(request, 'checkout/checkout.html')


def checkout_success(request):
    return render(request, 'checkout/checkout-success.html')


def checkout_failed(request):
    return render(request, 'checkout/checkout-failed.html')