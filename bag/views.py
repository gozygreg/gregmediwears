from django.shortcuts import render


def bag_summary(request):
    """ A view that renders the bag contents page """
    return render(request, 'bag/bag-summary.html')


def bag_add(request):
    pass


def bag_delete(request):
    pass


def bag_update(request):
    pass
