from django.shortcuts import render
from order.models import Order, OrderItems
from django.contrib.auth.decorators import login_required


@login_required
def order_register(request):
    cart = request.user.profile.cart
    new_order = Order(cart=cart)    # Construct new Order object for cart model
    new_order.save()

    """
    Below For block copies all CartItem objects into OrderItem model.
    Note that we use related name rollback method to get CartItem
    model objects from current Cart object
    """
    cart_items = cart.items.filter(cart=cart)   # Get all Items in customer's cart
    OrderItems.objects.filter(order=new_order).delete()   # Delete all items if there are any in OrderItem
    for item in cart_items:
        new_order_items = OrderItems(order=new_order,
                                     product=item.product,
                                     price=item.price,
                                     quantity=item.quantity)
        print(new_order_items)
        #new_order_items.save()     # This line makes new OrderItem object but for test purpose we comment this off!

    new_order_items = OrderItems.objects.all()
    return render(request, 'order_register.html',
                  {'order': new_order,
                   'order_items': new_order_items})

