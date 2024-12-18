from django.urls import path

from .views import (ProductListView, ProductDetailView, ProductCreateView,
                    ProductUpdateView, ProductDeleteView, CategoryListView,
                    CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
                    BrandListView, BrandCreateView, BrandUpdateView,
                    BrandDeleteView)

app_name = "products"

urlpatterns = [
    # Category
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("categories/create/", CategoryCreateView.as_view(), name="category_create"),
    path("categories/<int:pk>/update/", CategoryUpdateView.as_view(), name="category_update"),
    path("categories/<int:pk>/delete/", CategoryDeleteView.as_view(), name="category_delete"),
    # Brand
    path("brands/", BrandListView.as_view(), name="brand_list"),
    path("brands/create/", BrandCreateView.as_view(), name="brand_create"),
    path("brands/<int:pk>/update/", BrandUpdateView.as_view(), name="brand_update"),
    path("brands/<int:pk>/delete/", BrandDeleteView.as_view(), name="brand_delete"),
    # Product
    path("products", ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"), 
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
]
