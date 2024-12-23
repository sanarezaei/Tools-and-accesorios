from django.shortcuts import render, redirect
from django.views.generic import  CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from django_filters.views import FilterView

from .forms import ProductForm, ProductFeatureForm, ProductImageForm, ProductImageFormSet
from .models import Product, Category, Brand
    
import django_filters


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__name", lookup_expr="icontains", label="Category")
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte", label="Min Price")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte", label="Max Price")
    
    # lookup_expr => expressions = حالت
    class Meta:
        model = Product
        fields = ["category", "price_min", "price_max"]


class ProductListView(FilterView):
    model = Product
    paginate_by = 20
    filterset_class = ProductFilter 
    template_name = "products/product_list.html"
    context_object_name = "products"
    
    def get_queryset(self):
        return Product.objects.filter(active=True)
    

class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin ,CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:product_list")
    
    def test_func(self):
        return self.request.user.is_superuser
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Product"
        return context


def create_product_view(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST)
        image_formset = ProductImageFormSet(request.POST, request.FILES)
        feature_form = ProductFeatureForm(request.POST)
        
        if product_form.is_valid() and image_formset.is_valid() and feature_form.is_valid():
            
            product = product_form.save()
            
            image_formset.instance = product
            image_formset.save()
            
            feature = feature_form.save(commit=False)
            feature.product = product
            feature.save()
            
            return redirect("products:product_list")
    else:
        product_form = ProductForm()
        image_formset = ProductImageFormSet()
        feature_form = ProductFeatureForm()
 
    return render(request, "products/create_product.html", {
        "product_form": product_form,
        "image_formset": image_formset,
        "feature_form": feature_form
    })


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
    success_url = reverse_lazy("products:product_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"