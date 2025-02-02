from django.contrib import messages
from django.db import transaction, models
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView

from azbankgateways import bankfactories, models as bank_models, default_settings as settings 

from accounts.models import Address
from .cart import Cart
from .models import OrderItem, Order
from products.models import Product


def get_cart_detail(cart):
    return [
        {
            "product": product, 
            "quantity": cart.get_quantities().get(str(product.id)),
            "total_amount": cart.get_quantities().get(str(product.id)) * product.price
        }
        for product in cart.get_products()
    ]


class CartsView(TemplateView):
    template_name = 'orders/cart_summary.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = Cart(self.request)
        context['cart_items'] = get_cart_detail(cart)
        context['cart_total'] = cart.cart_total()
        return context


class CartUpdateView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        operation = request.POST.get("operation", "add")
        
        cart = Cart(request)
        result = cart.add_or_update(product_id=product_id, operation=operation, quantity=quantity)
            
        if result:
            messages.success(request, "Cart updated successfully with operation: {operation}!")
        else:
            messages.error(request, "Unable to update cart. Product may be out of quantity.")
        
        return redirect('orders:cart_summary')


class CartRemoveView(View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")

        cart = Cart(request)
        cart.delete(product_id=product_id)

        return redirect('orders:cart_summary')
    

def order_create_view(request):
    cart = Cart(request)
    
    if not request.user.is_authenticated:
        return redirect("login")
    
    user_address = Address.objects.filter(user=request.user)
    if not user_address.exists():
        return redirect("accounts:address_create")
    
    address = user_address.first()
    
    order = Order.objects.create(
        customer=request.user, 
        address=address, 
    )
    
    for product_id, quantity in cart.get_quantities().items():
        product = get_object_or_404(Product, id=product_id)
    
        OrderItem.objects.create(
            order=order,
            product=product, 
            quantity=quantity,
            price=product.price
        )
        
        cart.clear()
        
        request.session["order_id"] = order.id
        return render(request, "orders/create_order.html")
