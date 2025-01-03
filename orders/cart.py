from django.shortcuts import get_object_or_404

from products.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('carts')

        if cart is None:
            cart = self.session['carts'] = {}
        
        self.cart = cart


    def add_or_update(self, product_id, quantity=1):
        product = get_object_or_404(Product, id=product_id)

        if product.check_quantity(quantity):

            self.cart[str(product_id)] = {
                'quantity': quantity,
                'total_amount': float(product.price) * quantity
            }
            self.session.modified = True

            return True
        return False


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

