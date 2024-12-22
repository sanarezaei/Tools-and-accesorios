from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django_filters.views import FilterView
import django_filters  # pip install django-filter

from .forms import ProductForm, CategoryForm, BrandForm
from .models import Product, Category, Brand

#
# class CategoryListView(ListView):
#     model = Category
#     template_name = "products/category_list.html"
#     context_object_name = "categories"
#
#
# class CategoryCreateView(CreateView):
#     model = Category
#     form_class = CategoryForm
#     template_name = "products/category_form.html"
#     success_url = reverse_lazy("products:category_list")
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Category Create"
#         return context
#
#
# class CategoryUpdateView(UpdateView):
#     model = Category
#     form_class = CategoryForm
#     template_name = "products/category_form.html"
#     success_url = reverse_lazy("products:category_list")
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Category Update"
#         return context
#
#
# class CategoryDeleteView(DeleteView):
#     model = Category
#     template_name = "products/category_confirm_delete.html"
#     success_url = reverse_lazy("products:category_list")
#
#
# class BrandListView(ListView):
#     model = Brand
#     template_name = "products/brand_list.html"
#     context_object_name = "brands"
#
#
# class BrandCreateView(CreateView):
#     model = Brand
#     form_class = BrandForm
#     template_name = "products/brand_form.html"
#     success_url = reverse_lazy("products:brand_list")
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Create Brand"
#         return context
#
#
# class BrandUpdateView(UpdateView):
#     model = Brand
#     form_class = BrandForm
#     template_name = "products/brand_form.html"
#     success_url = reverse_lazy("products:brand_list")
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Brand Update"
#         return context
#
#
# class BrandDeleteView(DeleteView):
#     model = Brand
#     template_name = "products/brand_confirm_delete.html"
#     success_url = reverse_lazy("products:brand_list")
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Delete Brand"
#         return context


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains', label='Category')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Min Price')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Max Price')

    class Meta:
        model = Product
        fields = ['category', 'price_min', 'price_max']


class ProductListView(FilterView):
    model = Product
    paginate_by = 20
    filterset_class = ProductFilter
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(active=True)


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
    success_url = reverse_lazy("products:product_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:product_list")

    # بررسی اینکه کاربر سوپریوزر است یا نه
    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Product"
        return context
    
    
# class ProductUpdateView(UpdateView):
#     model = Product
#     form_class = ProductForm
#     template_name = "products/product_form.html"
#     success_url = reverse_lazy("products:product_list")
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Edit Product"
#         return context
#
#
# class ProductDeleteView(DeleteView):
#     model = Product
#     template_name = "products/product_confirm_delete.html"
#     success_url = reverse_lazy("products:product_list")
