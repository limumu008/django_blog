from django.contrib import messages
from django.shortcuts import render, redirect

from cart.cart import Cart
from order.forms import OrderForm
from order.models import OrderItem
from .tasks import order_created


def create_order(request):
    """使用 cart 的数据创建 order"""
    cart = Cart(request)
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            # create order
            order = order_form.save(commit=False)
            order.customer = request.user
            order.email = request.user.email
            order.save()
            # create order_item
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            # send mail by celery
            order_created.delay(order.id)
            messages.success(request, '结算成功，请继续享受购物吧~')
            return redirect('shop:product_list')
    else:
        order_form = OrderForm()
    return render(request, 'order/create.html', {'order_form': order_form, 'cart': cart})
