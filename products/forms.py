from django import forms 
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from .models import ProductFeature, Product, Brand, Category, ProductImage, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "body"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "brand", "name", "description", "price", "quantity", "discount", "active", "slug"]
        
    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if slug and Product.objects.filter(slug=slug).exists():
            raise ValidationError("This slug is already in use. Please choose another.")
        return slug


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["image"]


ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    extra=1,
    can_delete=True
)


class ProductFeatureForm(forms.ModelForm):
    class Meta:
        model = ProductFeature
        fields = ["material", "engine_type", "battery_voltage", "battery_type",
                  "number_of_speeds", "charging_time", "weight", "height"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "body"]    