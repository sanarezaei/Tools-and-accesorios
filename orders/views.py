from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from accounts.models import Address
from .cart import Cart
from .models import OrderItem, Order, Payment


class CartsView(TemplateView):
    template_name = 'orders/cart_summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = Cart(self.request)
        context['cart_items'] = [
            {
                "product": product, 
                "quantity": cart.get_quantities().get(str(product.id)),
                "total_amount": cart.get_quantities().get(str(product.id)) * product.price
            }
            for product in cart.get_products()
        ]
        
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
    

class OrderCreateView(View):
    def get(self, request):
        cart = Cart(request)
        if cart is None:
            messages.error(request, "Your cart is empty")
            return redirect("cart_summary")
        
        addresses = Address.objects.filter(user=request.user)
        if not addresses.exists():
            messages.error(request, "Please add address before creating an order.")
            return redirect("accounts:address_create")
        
        return render(request, "orders/create_order.html", {
            "cart": cart, 
            "addresses": addresses,
        })
    
    @transaction.atomic   
    def post(self, request):
        cart = Cart(request)
        if cart is None:
            messages.error(request, "Your cart is empty.")
            return redirect("orders:cart_summary")
    
        address_id = request.POST.get("address")
        address = get_object_or_404(Address, id=address_id, user=request.user)
        
        try:
            # create the order
            order = Order.objects.create(
                customer=request.user, 
                status=Order.ORDER_STATUS_UNPAID,
            )   
              
            # add items to the order 
            for product in cart.get_products():
                quantity = cart.cart[str(product.id)]["quantity"]
                if not product.check_quantity(quantity):
                    messages.error(request, f"Insufficient stock for {product.name}")
                    raise ValueError("Insufficient stock")

                OrderItem.objects.create(
                    order=order, 
                    product=product, 
                    price=product.price,
                    quantity=quantity,
                )
                # Reduce inventory after the order is confirmed
                product.reduce_quantity(quantity)
                
            # Create the cart after order creation
            cart.cart.clear()
            cart.session.modified = True
            
            messages.success(request, f"Order {order.code} created successfully.")
            return redirect("order_detail", order_id=order.id)
        
        except Exception:
            transaction.set_rollback(True)
            messages.error(request, f"Failed to create the order: {Exception}")    
            return redirect("orders:cart_summary") 
        
          
class OrderPayView(DetailView):
    
    @transaction.atomic
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, customer=request.user, status=Order.ORDER_STATUS_UNPAID)
        
        try:
            payment_success =  process_payment(order) 
            # Assume process_payment is a  for payment handling
            
            if payment_success:
                order.status = Order.ORDER_STATUS_PAID
                order.save()
                
                Payment.objects.create(
                    order=order,
                    amount=order.items.aggregate(total=models.Sum(models.F("price") * models.F("quantity")))["total"],
                    status="success"
                )
                
                messages.success(request, f"Order {order.code} has been successfully paid.")
                return redirect("order_detail", order_id=order.id)    
            else:
                raise ValueError("Payment failed.")
            
        except Exception:
            transaction.set_rollback(True)
            messages.error(request, f"Payment failed: {str(Exception)}")
            return redirect("order_detail", order_id=order.id)
            

class OrderDetailView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, customer=request.user)
        order_items = OrderItem.objects.filter(order=order)
        
        return render(request, "order:order_detail.html", {
            "order": order,
            "order_items": order_items,
        })
