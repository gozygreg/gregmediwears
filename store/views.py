from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from . models import Category, Product, ReviewRating
from checkout.models import Order, OrderLineItem
from django.contrib import messages
from django.db.models import Q
from .forms import ReviewForm


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

    try:
        order_line_item = OrderLineItem.objects.get(product=product, order__user=request.user)
        order = order_line_item.order
    except OrderLineItem.DoesNotExist:
        order = None

    # Get the reviews 
    reviews = ReviewRating.objects.filter(product=product, status=True)
    context = {
        'product': product,
        'order': order,
        'reviews': reviews,
    }
    return render(request, 'store/product-info.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you. Your review is updated')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted')
                return redirect(url)
