from products.models import Product


class Cart:
   def __init__(self, request):
      self.session = request.session
      
      cart = self.session.get("session_key")
      
      if session_key not in cart:
         cart = self.session["session_key"] = {}
         
      self.cart = cart 
      
   def add(self, product):
      product_id = str(product_id)
      
      if product_id in self.cart:
         pass
      else:
         self.cart[product_id] = {"price": str(product.price)} 
         
      self.session.modified = True     
   
   def __len__(self):
      return len(self.cart)
   
   def get_products(self):
      # get ids from the cart
      product_ids = self.cart.keys()
      # use ids to lookup products in  database model
      products = Products.objects.filter(id__in=product_ids)
      return products
   
   def get_quantities(self):
      quantities = self.cart
      return quantities
   
   def update(self, product, quantity):
      product_id = str(product_id)
      product_qty = int(quantity)
      
      #get cart 
      our_cart = self.cart
      # update dictionary/cart
      our_cart[product_id] = product_qty
      
      self.session.modified = True
      
      thing = self.cart
      return thing
   
   def delete(self, product):
      product_id = str(product)
      
      if product_id in self.cart:
         # delete from dictionary/cart
         del self.cart[product_id]
         
      self.session.modified = True
      
   def cart_total(self):
      #get products IDS
      product_ids = self.cart.keys()
      # lookup those keys in our products database
      products = Product.objects.filer(id__in=product_ids)
      # get quantities
      quantities = self.cart
      # start counting at 0 
      total = 0
      
      for key, value in quantities.items():
         # convert key string into so we can do math
         key = int(key)
         for product in products:
            if product_id == key:
               total = total + (product.price * value)
      return total
   
def cart(request):
   return {"cart": Cart(request)}
