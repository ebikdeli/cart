from django.db import models
from mainapp.models import Product, Profile
from decimal import Decimal
from django.core import validators

"""
This cart is unique for every user. After the user
register the order, Cart model got empty for later
use
"""
class Cart(models.Model):
    customer = models.OneToOneField(Profile,
                                    on_delete=models.CASCADE,
                                    related_name='cart')
    total_quantity = models.PositiveIntegerField(verbose_name='numbers of products in the cart: ',
                                                 default=0, blank=True,
                                                 validators=[validators.MaxValueValidator(100,'You can\'t order more than 100 items')])
    total_price = models.DecimalField(max_digits=7, decimal_places=0,
                                      default=Decimal(0), blank=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Cart'
        ordering = ['-updated']

    def __str__(self):
        if self.customer.user.first_name and self.customer.user.last_name:
            return 'This cart belongs to ' + self.customer.user.first_name + ' ' + self.customer.user.last_name
        return 'This cart belongs to ' + self.customer.user.username

"""
CartItem handles every item we add to the cart.
It holds item name, quantity and price.
"""
class CartItem(models.Model):
        QUANTITY_CHOICE = [(number, str(number)) for number in range(1, 21)]
        cart = models.ForeignKey(Cart,
                                 on_delete=models.CASCADE,
                                 related_name='items')
        product = models.ForeignKey(Product,
                                    related_name='cart',
                                    on_delete=models.CASCADE)
        quantity = models.PositiveIntegerField(default=0,
                                               choices=QUANTITY_CHOICE)
        price = models.DecimalField(max_digits=6, decimal_places=0, blank=True)
        created = models.DateTimeField(auto_now_add=True)
        updated = models.DateTimeField(auto_now=True)

        class Meta:
            db_table = 'Cart_Item'
            ordering = ['price', 'quantity', 'cart']

        def __str__(self):
            first_name = self.cart.customer.user.first_name
            last_name = self.cart.customer.user.last_name
            user_name = self.cart.customer.user.username
            if first_name and last_name:
                return 'Customer: ' + first_name + ' ' + last_name + ', Item: ' + self.product.name
            return 'Customer: ' + user_name + ', Item: ' + self.product.name

        def save(self, *args, **kwargs):
            if self.quantity:
                self.price = self.quantity * self.product.unit_price  # We use Product unit_price field and
            super().save(*args, **kwargs)  # Product quantity field here
