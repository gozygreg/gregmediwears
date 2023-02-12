from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        creates custom url so that users can be redirected to
        specific category page
        """
        return reverse('list-category', args=[self.slug])


class Product(models.Model):
    # Foreign key
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    brand = models.CharField(max_length=255, default='gmwears')
    image = models.ImageField(null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        creates custom url so that users can be redirected to
        specific product page
        """
        return reverse('product-info', args=[self.slug])
