from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse

from .models import Order, OrderItem
from products.models import Product
from .cart import Cart


class CartView(TemplateView):
    template_name = "order/cart.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = Cart(self.request)
        context['carts'] = cart.all_products()

        return context
       
 
class AddCartView(View):
    def get(self, request, *args, **kwargs):
        product_id = str(kwargs["product_id"])

        cart = Cart(request)
        cart.add_product(product_id, quantity=1)

        return redirect("order:all_carts")


class RemoveFromCartView(View):
    def get(self, request, *args, **kwargs):
        product_id = str(kwargs["product_id"])

        cart = Cart(request)
        cart.remove(product_id)

        return redirect("order:all_carts")
    















# class FinalizeOrderView(View):
#     def post(self, request, *args, **kwargs):
#         cart = request.session.get("cart", {})
#         if not cart:
#             return JsonResponse({"error": "cart is empty"}, status=400)
#
#         order = Order.objects.create()
#         for product_id, quantity in cart.items():
#             product = get_object_or_404(Product, id=product_id)
#             OrderItem.objects.create(order=order, product=product, quantity=quantity)
#
#         request.session["cart"]
#         return JsonResponse({"message": "Order placed successfully", "order_id": order.id})
