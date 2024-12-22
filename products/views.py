from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from .forms import ProductForm, CategoryForm, BrandForm
from .models import Product, Category, Brand


class CategoryListView(ListView):
    model = Category
    template_name = "accounts/category_list.html"
    context_object_name = "categories"


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "products/category_form.html"
    success_url = reverse_lazy("products:category_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Category Create"
        return context
    

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "products/category_form.html"
    success_url = reverse_lazy("products:category_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Category Update"
        return context
    

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "products/category_confirm_delete.html"
    success_url = reverse_lazy("products:category_list")

class BrandListView(ListView):
    model = Brand
    template_name = "products/brand_list.html"
    context_object_name = "brands"
    

class BrandCreateView(CreateView):
    model = Brand
    form_class = BrandForm
    template_name = "products/brand_form.html"
    success_url = reverse_lazy("products:brand_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Brand"
        return context
 
   
class BrandUpdateView(UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = "products/brand_form.html"
    success_url = reverse_lazy("products:brand_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Brand Update"
        return context
    

class BrandDeleteView(DeleteView):
    model = Brand
    template_name = "products/brand_confirm_delete.html"
    success_url = reverse_lazy("products:brand_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Brand"
        return context
    

class ProductListView(ListView):
    model = Product
    queryset = Product.objects.filter(active=True)
    template_name = "products/product_list.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
    success_url = reverse_lazy("products:product_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:product_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Product"
        return context
    
    
class ProductUpdateView(UpdateView):
    model = Product
    fields = ["category", "brand", "name", "description", "price", "quantity", "discount", "price", "active"]
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:product_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Product"
        return context
    

class ProductDeleteView(DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("products:product_list")
