from django.urls import path


from .views import CartsView, CartUpdateView, CartRemoveView, order_create_view

app_name = "orders"

urlpatterns = [
    path("carts/", CartsView.as_view(), name="cart_summary"),
    path("cart/delete/<str:product_id>/", CartRemoveView.as_view(), name="cart_delete"),
    path("cart/update/", CartUpdateView.as_view(), name="cart_update"),
    path("create/", order_create_view, name="create_order"),
]
