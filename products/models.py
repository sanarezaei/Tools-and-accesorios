from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

import random

class Category(MPTTModel):
    parent = TreeForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="Children")
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category_images/", blank=True, null=True)

    def __str__(self):
        return self.name 
    

class Brand(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="brand_images/", blank=True, null=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS = (
        ("True", "available"),
        ("False", "non-existent"),
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="category")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    discount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    active = models.CharField(max_length=5, choices=STATUS, default=False)
    
    def __str__(self):
        return self.name


class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    class Meta:
        verbose_name = "Product Feature"
        verbose_name_plural = "Product Features"
        
    def __str__(self):
        return f"{self.product} - {self.key}: {self.value}"