from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from azbankgateways import bankfactories, models as bank_models, default_settings as settings 

from accounts.models import Address
from .cart import Cart
from .models import OrderItem, Order, Payment

import factory
import logging

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
    

class OrderCreateView(View):
    def get(self, request):
        cart = Cart(request)
        if cart is None:
            messages.error(request, "Your cart is empty")
            return redirect("cart_summary")
        
        addresses = Address.objects.filter(user=request.user.id)
        if not addresses.exists():
            messages.error(request, "Please add address before creating an order.")
            return redirect("accounts:address_create")
        
        return render(request, "orders/create_order.html", {
            "cart_items": get_cart_detail(cart),
            "addresses": addresses,
            "cart_total": cart.cart_total()
        })
    
    @transaction.atomic   
    def post(self, request):
        print('=========================================')
        cart = Cart(request)
        if cart is None:
            messages.error(request, "Your cart is empty.")
            return redirect("orders:cart_summary")

        print(cart)
        
        address = request.POST.get("address")
        address = get_object_or_404(Address, user=request.user)
        
        print(address)
        
        try:
            # create the order
            print("create")
            order = Order.objects.create(
                customer=request.user, 
                status=Order.ORDER_STATUS_UNPAID,
            )   
            print(order)
              
            # add items to the order 
            for product in cart.get_products():
                quantity = cart.cart[str(product.id)]["quantity"]
                print("q:", quantity, "p:", product)
                
                if not product.check_quantity(quantity):
                    messages.error(request, f"Insufficient stock for {product.name}")
                    return redirect("orders:cart_summary")

                OrderItem.objects.create(
                    order=order, 
                    product=product, 
                    price=product.price,
                    quantity=quantity,
                )
                # Reduce inventory after the order is confirmed
                product.reduce_quantity(quantity)
                
            # Clear the cart after order creation
            cart.cart.clear()
            cart.session.modified = True
            print("Done")
            messages.success(request, f"Order {order.code} created successfully.")
            return redirect("pages:home")
        
        except Exception as e:
            transaction.set_rollback(True)
            messages.error(request, f"Failed to create the order: {str(e)}")    
            return redirect("orders:cart_summary") 

           
class OrderPayView(DetailView):
    
    @transaction.atomic
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, customer=request.user, status=Order.ORDER_STATUS_UNPAID)
        
        amount = Order.objects.filter("cart_total")
        bank = factory.create()
    
        try:
            factory = bankfactories.BankFactory()
            bank.set_request(request)
            bank.set_amount(amount)
            payment_success = bank.set_client_callback_url(reverse('orders:callback-gateway'))
            
            if payment_success:
                order.status = Order.ORDER_STATUS_PAID
                order.save()
                
                Payment.objects.create(
                    order=order,
                    amount=order.items.aggregate(total=models.Sum(models.F("price") * models.F("quantity")))["total"],
                    status="success"
                )
                
                messages.success(request, f"Order {order.code} has been successfully paid.")
                return bank.redirect_gateway()
            else:
                raise ValueError("Payment failed.")
            
        except Exception:
            transaction.set_rollback(True)
            messages.error(request, f"Payment failed: {str(Exception)}")
            return redirect("order_detail", order_id=order.id)
    
    
    def callback_gateway_view(request):
        tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
        if not tracking_code:
            logging.debug("لینک معتبر نیست.")
            raise Http404

        try:
            bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
            
        except bank_models.Bank.DoesNotExist:
            logging.debug(" لینک معتبر نیست")
            raise Http404

        if bank_record.is_success:
            return HttpResponse("با موفقیت انجام شد.")
        return HttpResponse(" با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")
        

class OrderDetailView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, customer=request.user)
        order_items = OrderItem.objects.filter(order=order)
        
        return render(request, "order:order_detail.html", {
            "order": order,
            "order_items": order_items,
        })
