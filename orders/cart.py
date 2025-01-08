from django.shortcuts import get_object_or_404

from products.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('carts')

        if cart is None:
            cart = self.session['carts'] = {}
        
        self.cart = cart

    def add_or_update(self, product_id, operation, quantity):
        product_id_str = str(product_id)
        product = get_object_or_404(Product, id=product_id)
              
        if operation == "add":
            new_quantity = quantity + 1
            if product.check_quantity(new_quantity):
                if product_id_str in self.cart:
                    self.cart[product_id_str]["quantity"] = new_quantity
                else:
                    self.cart[product_id_str] = {
                        "quantity": 1,
                    }
            else:
                return False
                   
        elif operation == "subtract":
            if product_id_str in self.cart: 
                self.cart[product_id_str]["quantity"] -= 1
                if self.cart[product_id_str]["quantity"] == 0:
                    del self.cart[product_id]
                    
            else: 
                return False
        
        self.session.modified = True
        return True


    def delete(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def get_products(self):
        return Product.objects.filter(id__in=self.cart.keys())

    def cart_total(self):
        total = 0
        for product in self.get_products():
            quantity = self.cart[str(product.id)]["quantity"]
            total += quantity * product.price
        return total

    def get_quantities(self):
        return {
            product_id: item['quantity'] for product_id, item in self.cart.items()
        } 

