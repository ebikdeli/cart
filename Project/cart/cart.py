from cart.models import CartItem
from django.shortcuts import get_list_or_404,redirect

"""
This function takes request object and calculates
'total_quantity' and 'total_price' fields of the user cart
all the changes to Cart object will done here
"""
def change_cart(request, cart_obj=None, cart_item_obj=None):
    if cart_obj is None:
        cart = request.user.profile.cart
    else:
        cart = cart_obj
    if cart_item_obj is None:
        try:
            cart_items = get_list_or_404(CartItem, cart=cart)
        except:     # If there is no item in the cart,
            cart.total_quantity = 0
            cart.total_price = 0
            cart.save()
            return redirect('cart:cart')
    else:
        cart_items = cart_item_obj

    """If we don't want the cart to count cart price
    and cart quantity again, We should assign 0 to the cart
    fields. then we update cart fields with current cart items
    quantity and price"""
    cart.total_quantity = 0
    cart.total_price = 0
    cart.save()

    for item in cart_items:
        cart.total_quantity += item.quantity
        cart.total_price += item.price
    cart.save()
