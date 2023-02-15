from django.shortcuts import render
from .bag import Bag
from store.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


def bag_summary(request):
    """ A view that renders the bag contents page """
    return render(request, 'bag/bag-summary.html')


def bag_add(request):

    bag = Bag(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        product = get_object_or_404(Product, id=product_id)

        bag.add(product=product, product_qty=product_quantity)

        response = JsonResponse(
            {
                'The product is called: ': product.name,
                ' and the product quantity is: ': product_quantity})
        return response


def bag_delete(request):
    pass


def bag_update(request):
    pass
