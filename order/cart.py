from urllib import request
from django.shortcuts import get_object_or_404

from products.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def all_products(self):
        return self.cart

    def add_product(self, product_id, quantity):
        product = get_object_or_404(Product, id=product_id)

        self.cart[product_id] = {
            'product_name': product.name,
            'quantity': quantity,
            'total_price': quantity * product.price
        }
        self.save()
        print(f'{quantity} of {product_id} added to cart.')

    def remove(self, product_id):
        del self.cart[product_id]
        self.save()
        print(f'{product_id} deleted from cart.')

    def save(self):
        self.session.modified = True

    def get_total_price(self):
        pass
        # calculate total price of all products in cart

    def clear(self):
        del self.session['cart']
        self.save()
