from django.db import models
from cart.models import Cart
from mainapp.models import Product
from django.utils import timezone


class Order(models.Model):
    cart = models.ForeignKey(Cart,
                             on_delete=models.CASCADE,
                             related_name='orders')
    order_quantity = models.PositiveIntegerField()
    order_price = models.DecimalField(max_digits=7, decimal_places=0)
    paid = models.BooleanField(default=False)
    pay_date = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'Order_order'
        ordering = ['-id', 'pay_date']

    def __str__(self):

        return 'You ordered ' + str(self.order_quantity) + ' items worth of ' + str(self.order_price) + ' Tomans'


    def save(self, *args, **kwargs):
        cart = self.cart
        self.order_quantity = cart.total_quantity
        self.order_price = cart.total_price
        super().save(*args, **kwargs)


class OrderItems(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='items')
    product = models.ForeignKey(Product,
                                related_name='order_item',
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=0)

    class Meta:
        db_table = 'Order_order_item'

    def __str__(self):
        return self.product.producer.name + '_' + self.product.name + " is on your the order"
