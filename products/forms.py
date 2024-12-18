from django import forms 

from .models import ProductFeature, Product, Brand, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["parent", "name", "image"]
        widget = {
            "parent":forms.TextInput(attrs={"class": "form-control", "placeholder": "Category Name "}),
            "name": forms.Select(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"})
        }


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["name", "image"]
        widget = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Brand Name"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"})
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "brand", "name", "description", "price", "quantity", "discount", "image", "active"]
        widget = {
            "category": forms.Select(attrs={"class": "form-control"}),
            "brand": forms.Select(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Product Name"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Product Description"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Price"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Quantity"}),
            "discount": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Discount"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "active": forms.Select(attrs={"class": "form-control"}),
        }


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["name", "image",]
        widget = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Brand Name"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"})
        }

class ProductFeatureForm(forms.ModelForm):
    class Meta:
        model = ProductFeature
        fields = ["product", "key", "value"]
        widget = {
            "key": forms.TextInput(attrs={"class": "form-class", "placeholder": "Feature Key"}),
            "value": forms.TextInput(attrs={"class": "form-class", "placeholder": "Feature Value"})
        }
