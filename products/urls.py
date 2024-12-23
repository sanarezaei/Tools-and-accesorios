from django.urls import path

from .views import ProductListView, ProductCreateView, ProductDetailView, create_product_view

app_name = "products"

urlpatterns = [
    # Product
    path("", ProductListView.as_view(), name="product_list"),
    # path("create/", ProductCreateView.as_view(), name="product_create"), 
    path("<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("create/", create_product_view, name="product_create"),
]
