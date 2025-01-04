from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views import View

from .cart import Cart


class CartsView(TemplateView):
    template_name = 'orders/cart_summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = Cart(self.request)
        context['cart_items'] = [
            {
                "product": product, 
                "quantity": cart.get_quantities().get(str(product.id), 1),
                "total_amount": cart.cart.get(str(product.id), {}).get("total_amount", 0),
            }
            for product in cart.get_products()
        ]
        context['cart_total'] = cart.cart_total()
        return context


class AddToCart(View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        operation = request.POST.get("operation", "add")

        cart = Cart(request)
        if operation == "subtract":
            result = cart.add_or_update(product_id=product_id, quantity=-quantity, operation=operation)
        else:
            result = cart.add_or_update(product_id=product_id, quantity=quantity, operation=operation)
            
        if result:
            messages.success(request, "Cart updated successfully with operation: {operation}!")
        else:
            messages.error(request, "Unable to update cart. Product may be out of quantity.")
        
        return redirect('orders:cart_summary')


class RemoveFromCart(View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")

        cart = Cart(request)
        cart.delete(product_id=product_id)

        return redirect('orders:cart_summary')
    
