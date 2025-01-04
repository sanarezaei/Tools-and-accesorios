from django.db import models

from accounts.models import CustomUser
from products.models import Product


class UnpaidOrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Order.ORDER_STATUS_UNPAID)


class Order(models.Model):
    ORDER_STATUS_PAID = "p"
    ORDER_STATUS_UNPAID = "u"
    ORDER_STATUS_CANCELED = "c"
    ORDER_STATUS = [
        (ORDER_STATUS_PAID, "Paid"),
        (ORDER_STATUS_UNPAID, "Unpaid"),
        (ORDER_STATUS_CANCELED, "Canceled"),
    ]
    customer = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="orders")
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default=ORDER_STATUS_UNPAID)
    
    objects = models.Manager()
    unpaid_orders = UnpaidOrderManager()
    
    def __str__(self):
        return f"Order id={self.id}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()
     
    