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
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="category")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    discount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    active = models.BooleanField()
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    def __str__(self):
        return self.name

    def is_exists(self):
        if quantity == 0:
            return f"None exists"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.id}"
    

class ProductFeature(models.Model):
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, blank=True, null=True)
    material = models.CharField(max_length=100, blank=True, null=True)
    engine_type = models.CharField(max_length=100, blank=True, null=True)
    battery_voltage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    battery_type = models.CharField(max_length=100, blank=True, null=True)
    number_of_speeds = models.IntegerField(blank=True, null=True)
    charging_time = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return f"Features of {self.product.name}" if self.product else "Unassigned Product Features"
    
    
    class Meta:
        verbose_name = "Product Feature"
        verbose_name_plural = "Product Features"
