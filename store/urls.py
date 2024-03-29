from django.urls import path
from . import views


urlpatterns = [
    # Store or homepage
    path('', views.store, name='store'),
    # product detail or individual product
    path('product/<slug:product_slug>/', views.product_info, name='product-info'),
    # Individual category
    path('search/<slug:category_slug>/', views.list_category, name='list-category'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),

]