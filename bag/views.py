from django.shortcuts import render
from .bag import Bag
from store.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


def bag_summary(request):
    """ A view that renders the bag contents page """
    bag = Bag(request)
    return render(request, 'bag/bag-summary.html')


def bag_add(request):
    """
    View to add product into shopping bag
    """
    bag = Bag(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        product = get_object_or_404(Product, id=product_id)

        bag.add(product=product, product_qty=product_quantity)

        """
        Gets the total qauntity of products (from session data)
        after adding a product into the shopping bag
        """
        bag_quantity = bag.__len__()

        response = JsonResponse({'qty': bag_quantity})
        return response


def bag_delete(request):
    """
    View to delete product from shopping bag
    """
    bag = Bag(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        bag.delete(product=product_id)

        """
        Gets the latest quantity and total price after
        removing a product from the shopping bag
        """
        bag_quantity = bag.__len__()
        bag_total = bag.get_total()

        response = JsonResponse({'qty': bag_quantity, 'total': bag_total})
        return response


def bag_update(request):
    """
    View to update items in shopping bag
    """
    bag = Bag(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        bag.update(product=product_id, qty=product_quantity)

        """
        Gets the latest quantity and total price after
        updating a product in the shopping bag
        """
        bag_quantity = bag.__len__()
        bag_total = bag.get_total()

        response = JsonResponse({'qty': bag_quantity, 'total': bag_total})
        return response
