from django.shortcuts import get_object_or_404

from products.models import Product



session = {
    'carts': {
        '1': {
            'quantity': 1,
            'total_amount': 2000
        },
        '2': {
            'quantity': 5,
            'total_amount': 10000
        }
    }
}


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

            # if product_id in self.cart:
                # self.cart[product_id]['quantity'] = quantity

            self.cart[product_id] = {
                'quantity': quantity,
                'total_amount': product.price * quantity
            }
            self.session.modified = True

            print(self.cart)
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
        pass


    def get_quantities(self):
        pass

      

def cart(request):
   return {"cart": Cart(request)}


