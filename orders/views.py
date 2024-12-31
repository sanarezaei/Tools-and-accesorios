from django.contrib import messages
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, View, FormView


from .cart import Cart


def cart_summary(request):
    # get the cart
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quantities
    totals = cart.cart_total()
    return render(request, "orders/cart_summary.html", 
                  {"cart_products": cart_products(),
                  "quantities": quantities(),
                  "totals": totals,
                  })

def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # initialize response to avoid undefined errors
    response = {"error": "Invalid request"}
    # test for POST
    if request.POST.get("action") == "post":
        # get stuff
        product_id = int(request.POST.get("product_id"))
        # lookup product in DB
        product = get_object_or_404(Product, id=product_id)
        # save to session
        cart.add(product=product)
        
        # get cart quantity
        cart_quantity = cart.__len__()
        
        # response = JsonResponse({"Product Name: ": product.name})
        response = {"quantity": cart_quantity}
    return JsonResponse(response)
        
def cart_delete(request):
    cart = Cart(request)
    
    if request.POST.get("action") == "post":
        #get stuff
        product_id = int(request.POST.get("product_id"))
        # call delete function in Cart
        cart.delete(product=product_id)
        
        response = JsonResponse({"product": product_id})
        # return redirect("cart_summary")
        return response
              
def cart_update(request):
    cart = Cart(request)
    
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))
        
        cart.update(product=product_id, quantity=product_qty)
        
        response = JsonResponse({"qty": product_qty})
        return response


# ===========================================================================================


class CartsView(TemplateView):
    template_name = 'orders/carts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = Cart(self.request)
        context['carts'] = cart.get_products()

        return context


class AddToCart(View):
    def get(self, request, *args, **kwargs):
        # product_id = request.POST.get("product_id")
        product_id = self.kwargs.get("product_id")
        quantity = request.POST.get("quantity", 1)

        cart = Cart(request)
        result = cart.add_or_update(product_id=product_id)

        if result:
            messages.error(request, "ezafe shod ")
            return redirect("orders:cart_summary")

        messages.error(request, "mojod nist ")
        return redirect("products:product_list")


class RemoveFromCart(View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")

        cart = Cart(request)
        cart.delete(product_id=product_id)

        return redirect('orders:cart_summary')













