from django.shortcuts import render, redirect, reverse, get_object_or_404
from . models import Category, Product
from django.contrib import messages
from django.db.models import Q


def store(request):
    all_products = Product.objects.all()
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You did not enter any search criteria!")
                return redirect(reverse('store'))               
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            all_products = all_products.filter(queries)
    context = {
        'all_products': all_products,
        'search_term': query,
        }
    return render(request, 'store/store.html', context)


def categories(request):
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}


def list_category(request, category_slug=None):
    """ A view to get individual ctagory details """
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/list-category.html', {
        'category': category,
        'products': products
    })


def product_info(request, product_slug):
    """ A view to get individual product details """
    product = get_object_or_404(Product, slug=product_slug)
    context = {
        'product': product
    }
    return render(request, 'store/product-info.html', context)