from django.urls import path
from .views import CartView, AddCartView, RemoveFromCartView


app_name = 'order'

urlpatterns = [
    path('carts/', CartView.as_view(), name='all_carts'),
    path('cart/add/<int:product_id>/', AddCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove_from_cart')
]
