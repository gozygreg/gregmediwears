from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    # Foreign key
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    brand = models.CharField(max_length=255, default='gmwears')
    image = models.ImageField(null=True, blank=True, upload_to='images/')

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name
