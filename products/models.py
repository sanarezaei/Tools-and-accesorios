from django.db import models
from mptt.fields import TreeForeignKey


class Category(models.Model):
    parent = TreeForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="Children")
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category_images/", blank=True, null=True)

    def __str__(self):
        return self.name 
    

# class Brand(models.Model):
#     name = models.CharField(max_length=100)
#     image = models.ImageField(upload_to="brand_images/", blank=True, null=True)
    
#     def __str__(self):
        # return self.name
