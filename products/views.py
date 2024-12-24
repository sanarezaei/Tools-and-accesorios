from django.shortcuts import render, redirect
from django.views.generic import  CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.forms import inlineformset_factory

from django_filters.views import FilterView

from .forms import ProductForm, ProductFeatureForm, ProductImageForm, ProductImageFormSet
from .models import Product, Category, Brand, ProductImage
from .filters import ProductFilter
    
import django_filters


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__name", lookup_expr="icontains", label="Category")
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte", label="Min Price")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte", label="Max Price")
    brand = django_filters.CharFilter(field_name="brand__name", lookup_expr="icontains", label="Brand")
    
    # lookup_expr => expressions = حالت
    class Meta:
        model = Product
        fields = ["category", "price_min", "price_max", "brand"]


class ProductListView(FilterView):
    model = Product
    paginate_by = 20
    filterset_class = ProductFilter 
    template_name = "products/product_list.html"
    context_object_name = "products"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.filterset.form
        return context
    
    

class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin ,CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:product_list")
    
    def test_func(self):
        return self.request.user.is_superuser
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            context["image_formset"] = ProductImageFormSet(self.request.POST, self.request.FILES)
            context["feature_form"] = ProductFeatureForm(self.request.POST)
        else:
            context["image_formset"] = ProductImageFormSet()
            context["feature_form"] = ProductFeatureForm() 
        return context

    def form_valid(self):
        context = self.get_context_data()
        image_formset = context["image_formset"]
        feature_form = context["feature_form"]
        
        if form.is_valid() and image_formset.is_valid() and feature_form.is_valid():
            self.object = form.saveI()
            
            image_formset.instance = self.object
            image_formset.save()
            
            feature = feature_form.save(commit=False)
            feature.product = self.object
            feature.save()
            
            return redirect("products:product_list")
        
        return self.form_invalid(form)
    
    
ProductImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=1)
          
class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
    success_url = reverse_lazy("products:product_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"
