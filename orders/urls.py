from django.urls import path

from .views import cart_add, cart_delete, cart_summary, cart_update, CartsView, AddToCart, RemoveFromCart

app_name = "orders"

urlpatterns = [
    # path("cart/", cart_summary, name="cart_summary"),
    # path("cart/add/", cart_add, name="cart_add"),
    # path("cart/delete/", cart_delete, name="cart_delete"),
    # path("cart/update/", cart_update, name="cart_update"),

    path("carts/", CartsView.as_view(), name="cart_summary"),
    path("cart/add/<str:product_id>/", AddToCart.as_view(), name="cart_add"),
    path("cart/delete/<str:product_id>/", RemoveFromCart.as_view(), name="cart_delete"),
]
