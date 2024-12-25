from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse

from .models import Order, OrderItem
from products.models import Product


# List Cart Items
class CartView(TemplateView):
    template_name = "order/cart.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get("cart", {})
        products = []
        total_price = 0
    
    for product, quantity in cart_item():
        product = get_object_or_404(Product, id=product_id)
        products.append({"product": product, "quantity": quantity})
        total_price += product.price * quantity
        
    context["products"] = products
    context["total_price"] = total_price
    return context
       
 
# Add a Product to the Cart
class AddCartView(View):
    def post(self, request, *args, **kwargs):
        product_id = str(kwargs["product_id"])
        cart = self.request.session.get("cart", {})
        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1
            
        request.session["cart"] = cart
        return redirect("cart_view")
    

# Remove a Product
class RemoveFromCartView(View):
    def post(self, request, *args, **kwargs):
        product = str(kwargs["product_id"])
        cart = self.request.session.get("cart", {})
        if product_id in cart:
            del cart[product_id]
        
        request.session["cart"] = cart 
        return redirect("cart_view")
    

class FinalizeOrderView(View):
    def post(self, request, *args, **kwargs):
        cart = request.session.get("cart", {})
        if not cart:
            return JsonResponse({"error": "cart is empty"}, status=400)
        
        order = Order.objects.create()
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
        
        request.session["cart"]
        return JsonResponse({"message": "Order placed successfully", "order_id": order.id})