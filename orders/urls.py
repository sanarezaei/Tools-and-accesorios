from django.urls import path

from azbankgateways.urls import az_bank_gateways_urls

from .views import CartsView, CartUpdateView, CartRemoveView, OrderCreateView

app_name = "orders"

urlpatterns = [
    path("carts/", CartsView.as_view(), name="cart_summary"),
    path("cart/delete/<str:product_id>/", CartRemoveView.as_view(), name="cart_delete"),
    path("cart/update/", CartUpdateView.as_view(), name="cart_update"),
    path("order/create/", OrderCreateView.as_view(), name="create_order"),
    path('bank/', az_bank_gateways_urls(), name="callback-gateway"),
]
