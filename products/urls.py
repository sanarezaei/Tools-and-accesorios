from django.urls import path

from .views import ProductListView, ProductCreateView, ProductDetailView

app_name = "products"

urlpatterns = [
    # Product
    path("", ProductListView.as_view(), name="product_list"),
    path("create/", ProductCreateView.as_view(), name="product_create"), 
    path("<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]
