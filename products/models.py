from django.db import models
from django.template.defaultfilters import slugify

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from autoslug import AutoSlugField

import random

class Category(MPTTModel):
    parent = TreeForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="Children")
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="name", unique=True)
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
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=0)
    discount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    def is_exists(self):
        if self.quantity == 0:
            return False
        return True
    
    def check_quantity(self, number):
        return self.quantity >= number

    def reduce_quantity(self, amount):
        if amount < 0:
            raise ValueError("Amount to reduce must be positive.")
    
        self.quantity -= amount
        self.save()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/")
    
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


class ApprovedCommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Comment.COMMENTS_STATUS_APPROVED)


class Comment(models.Model):
    COMMENTS_STATUS_WRITING = 'writing'
    COMMENTS_STATUS_APPROVED = 'approved'
    COMMENTS_STATUS_NOT_APPROVED = 'not_approved'
    COMMENTS_STATUS = [
        (COMMENTS_STATUS_WRITING, "w"),
        (COMMENTS_STATUS_APPROVED, "a"),
        (COMMENTS_STATUS_NOT_APPROVED, "na"),
    ]   
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=255)
    body = models.TextField()
    status = models.CharField(max_length=12, choices=COMMENTS_STATUS, default=COMMENTS_STATUS_WRITING)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    approve = ApprovedCommentManager()