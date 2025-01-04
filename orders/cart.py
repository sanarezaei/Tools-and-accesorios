from django.shortcuts import get_object_or_404

from products.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('carts')

        if cart is None:
            cart = self.session['carts'] = {}
        
        self.cart = cart


    def add_or_update(self, product_id, quantity=1, operation='add'):
        product = get_object_or_404(Product, id=product_id)
        product_id_str = str(product_id)
        
        # Determine the current quantity in the cart
        current_quantity = self.cart.get(product_id_str, {}).get('quantity', 0)
        
        # Apply the operation        
        if operation == "add":
            new_quantity = current_quantity + quantity
        elif operation == "subtract":
            new_quantity = new_quantity - quantity
        else: # Default: set quantity
            new_quantity = quantity
            
        if new_quantity > 0 and product.check_quantity(new_quantity): 
            self.cart[product_id_str] = {
                "quantity": new_quantity, 
                "total_amount": float(product.price) * new_quantity,
            }
        elif new_quantity <= 0:
            # Remove item if quantity is 0 or less
            self.cart.pop(product_id_str, None)
        else:
            return False # Quantity exceeds stock
            
        self.session.modified = True

        return True


    def delete(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def get_products(self):
        print(self.cart.keys())
        return Product.objects.filter(id__in=self.cart.keys())


    def cart_total(self):
        return sum(item['total_amount'] for item in self.cart.values())


    def get_quantities(self):
        print(f"Cart contents: {self.cart}")
        return {product_id: item['quantity'] for product_id, item in self.cart.items()} 


def cart(request):
   return {"cart": Cart(request)}

