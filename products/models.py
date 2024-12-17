from django.db import models
from mptt.fields import TreeForeignKey

import random

class Category(models.Model):
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


class ProductFeature(models.Model):
    product = models.ForeignKey("Product", on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    key = models.CharField(max_length=100, help_text="Enter the feature key.")
    value = models.CharField(max_length=100, help_text="Enter the feature value.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Product Feature"
        verbose_name_plural = "Product Features"
        ordering = ["-created_at"]
        
    def __str__(self):
        return f"{self.product} - {self.key}: {self.value}"


class Product(models.Model):
    STATUS = (
        ("True", "available"),
        ("False", "non-existent"),
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="category")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, blank=True, null=True)
    feature = models.ForeignKey(ProductFeature, on_delete=models.CASCADE, blank=True, null=True, related_name="product_feature")
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    discount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    active = models.CharField(max_length=5, choices=STATUS, default=False)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # If the ID is not set, generate it
        if not self.product_id:
            self.product_id = self.generate_product_id()
        super().save(*args, **kwargs)
    
    def generate_product_id(self):
        # Generate ID as "xxxxx/yy"
        random_part = random.randint(10000, 99999)
        suffix_part = random.randint(10, 99) 
        return f"{random_part}/{suffix_part}"
