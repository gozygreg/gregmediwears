from django.shortcuts import render


def checkout(request):
    return render(request, 'checkout/checkout.html')


def checkout_success(request):
    return render(request, 'checkout/checkout-success.html')


def checkout_failed(request):
    return render(request, 'checkout/checkout-failed.html')