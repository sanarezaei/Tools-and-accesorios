from django.contrib import messages
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, View, FormView

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
        new_quantity = int(request.POST.get("quantity", 1))

        cart = Cart(request)
        current_quantity = cart.cart.get(str(product_id), {}).get("quantity", 0)
        update_quantity = current_quantity + new_quantity
        
        result = cart.add_or_update(product_id=product_id, quantity=update_quantity)

        if result:
            messages.success(request, "Product added to cart successfully!")
            return redirect("orders:cart_summary")
        else:
            messages.error(request, "Product is out of stock or unavailable.")
            return redirect("products:product_list")
        
        print("Redirecting to cart summary page")
        return reverse_lazy("orders:cart_summary")


class RemoveFromCart(View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")

        cart = Cart(request)
        cart.delete(product_id=product_id)

        return redirect('orders:cart_summary')
    
