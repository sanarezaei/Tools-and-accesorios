from django.urls import path

from .views import CartsView, AddToCart, RemoveFromCart

app_name = "orders"

urlpatterns = [
    path("carts/", CartsView.as_view(), name="cart_summary"),
    path("cart/add/<str:product_id>/", AddToCart.as_view(), name="cart_add"),
    path("cart/delete/<str:product_id>/", RemoveFromCart.as_view(), name="cart_delete"),
]
