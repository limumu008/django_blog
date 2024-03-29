from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from coupons.models import Coupon
from django_blog import settings
from shop.models import Product


class Order(models.Model):
    """一份订单：包括顾客，地址，是否支付，以及外键所有物品"""
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    address = models.CharField(max_length=200)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)

    coupon = models.ForeignKey(Coupon,
                               on_delete=models.SET_NULL,
                               related_name='orders',
                               null=True,
                               blank=True)
    discount = models.PositiveIntegerField(default=0,
                                           validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Order {self.id}"

    def get_total_price(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * self.discount / 100


class OrderItem(models.Model):
    """订单中的条目"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.order}:{self.product.name}:{self.price}:{self.quantity}"

    def get_cost(self):
        return self.price * self.quantity
