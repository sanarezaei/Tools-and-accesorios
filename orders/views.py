from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect

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

    