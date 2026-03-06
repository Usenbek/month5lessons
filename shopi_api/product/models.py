from django.db import models
from users.models import CustomUser
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='products') 
    owner = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


CHOICES = [(i, i) for i in range(1, 6)]

class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    stars = models.IntegerField(default=5, choices=CHOICES)

    def __str__(self):
        return f"Review for {self.product.title}"

