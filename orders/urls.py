from django.urls import path

from .views import cart_add, cart_delete, cart_summary, cart_update

app_name = "orders"

urlpatterns = [
    path("cart/", cart_summary, name="cart_summary"),
    path("cart/add/", cart_add, name="cart_add"),
    path("cart/delete/", cart_delete, name="cart_delete"),
    path("cart/update/", cart_update, name="cart_update"),
]
