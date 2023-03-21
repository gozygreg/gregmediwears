from django.contrib import admin
from . models import Category, Product, ReviewRating


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = (
        'name',
        'brand',
        'slug',
        'description',
        'price',
    )


admin.site.register(ReviewRating)
