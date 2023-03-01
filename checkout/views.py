from django.shortcuts import render, redirect, reverse
from .models import ShippingAddress
from .forms import ShippingForm
from bag.bag import Bag


# def checkout(request):
#     bag = Bag(request)
#     # users with accounts -- pre-fill the form
#     if request.user.is_authenticated:
#         try:
#             # Authenticated users with shipping information
#             shipping_address = ShippingAddress.objects.get(user=request.user.id)
#             context = {'shipping': shipping_address}
#             return render(request, 'checkout/checkout.html', context=context)
#         except:
#             # Authenticated users without shipping information
#             return render(request, 'checkout/checkout.html')
#     else:
#         # Guest user
#         return render(request, 'checkout/checkout.html')



#     return render(request, 'checkout/checkout.html')


def checkout(request):
    bag = Bag(request) 
    # If user is authenticated
    if request.user.is_authenticated:
        try:
            # Get the user's shipping address if it exists
            shipping_address = ShippingAddress.objects.get(user=request.user)
        except ShippingAddress.DoesNotExist:
            shipping_address = None
    else:
        shipping_address = None    
    if request.method == 'POST':
        # Process the form submission
        form = ShippingForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            request.session['shipping_address'] = shipping_address.id
            return redirect(reverse('dashboard'))
    else:
        # Render the form
        form = ShippingForm(instance=shipping_address)

    context = {
        'form': form,
        'shipping_address': shipping_address,
        'bag': bag,
        'stripe_public_key': 'pk_test_51MX7x2AGFYQzGfhGw5CWd6b1MlJ3C11whROQsiK8AcK31fXPYq35F7kgNlZBwE8wRpjIAyrYjeLwOgYqY6YnRsEK00JcAoHlHd',
        'client_secret': 'test client secret',
    }

    return render(request, 'checkout/checkout.html', context=context)










def checkout_success(request):
    return render(request, 'checkout/checkout-success.html')


def checkout_failed(request):
    return render(request, 'checkout/checkout-failed.html')