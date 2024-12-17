from django.db import models
from mptt.fields import TreeForeignKey


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
    product = models.CharField(max_length=200, help_text="Enter the product name") 
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
