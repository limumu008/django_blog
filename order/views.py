from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

from account.models import User
from cart.cart import Cart
from django_blog import settings
from order.forms import OrderForm
from order.models import OrderItem, Order
from shop.recommender import Recommender
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
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            # create order_item
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            # store order id
            request.session['order_id'] = order.id
            # send notice mail by celery
            order_created.delay(order.id)
            # 推荐计分
            recommender = Recommender()
            recommender.cal_products_bought([item.product for item in order.items.all()])
            # 重定向到支付页
            return redirect('order:payment_process')
    else:
        order_form = OrderForm()
    return render(request, 'order/create.html', {'order_form': order_form, 'cart': cart})


def payment_process(request, order_id=None):
    """process order with paypal"""
    try:
        # 立即购买
        order_id = request.session['order_id']
        del request.session['order_id']
    except KeyError:
        # 之后支付
        order_id = order_id
    order = get_object_or_404(Order, id=order_id)
    paypal_dict = {
        # 商家邮箱
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        # 总价
        "amount": order.get_total_price(),
        # 商品名
        "item_name": f"Order:{order.id}",
        # 识别码
        "invoice": str(order.id),
        # PayPal
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        # 支付成功后的重定向视图
        "return": request.build_absolute_uri(reverse('order:pay_done')),
        #  支付取消或其他
        "cancel_return": request.build_absolute_uri(reverse('order:pay_canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {'form': form}
    return render(request, 'order/payment.html', context)


@csrf_exempt
def payment_done(request):
    return render(request, 'order/pay_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'order/pay_canceled.html')


class OrderPaidView(generic.ListView):
    template_name = 'order/list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        orders_paid = Order.objects.filter(customer=user, is_paid=True).prefetch_related('items')
        return orders_paid


class OrderNotPaidView(generic.ListView):
    template_name = 'order/list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        orders_paid = Order.objects.filter(customer=user, is_paid=False).prefetch_related('items')
        return orders_paid
