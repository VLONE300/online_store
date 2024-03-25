from django.db import models

from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Seller(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    contact = models.CharField(max_length=500)


class Discount(models.Model):
    name = models.CharField(max_length=100)
    percent = models.PositiveIntegerField()
    date_start = models.DateField()
    date_end = models.DateField()


class Promocode(models.Model):
    name = models.CharField(max_length=100)
    percent = models.PositiveIntegerField()
    date_start = models.DateField()
    date_end = models.DateField()
    is_cumulative = models.BooleanField()


class Product(models.Model):
    name = models.CharField(max_length=100)
    article = models.CharField(max_length=100)
    description = models.TextField()
    count_on_stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Promocode, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()


class Order(models.Model):
    STATUSES = (
        ('In Progress', 'In Progress'),

    )
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100)