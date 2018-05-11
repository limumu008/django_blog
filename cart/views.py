from django.contrib import messages
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from cart.cart import Cart
from coupons.forms import CouponForm
from coupons.models import Coupon
from shop.models import Product


@require_POST
def change_cart(request):
    """
    根据 post 的 action 选择行动：增加/减少/移除 product，或者 clear cart。
    根据 post 的 product_id 选择操作的 product。
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=request.POST.get('product_id'))
    # 添加 product 到 cart
    if request.POST.get('action') == 'add_product':
        cart.add(product)
        return JsonResponse({'status': 'add_success'})
    # remove cart 中的 product
    elif request.POST.get('action') == 'remove_product':
        this_price = product.price * int(cart[request.POST.get('product_id')]['quantity'])
        cart.remove(product)
        return JsonResponse({'status': 'rm_success', 'this_price': this_price})
    elif request.POST.get('action') == 'clear_cart':
        cart.clear()
    # 修改 cart 中 product 数量 --not ajax
    else:
        quantity = int(request.POST.get('quantity'))
        cart.change(product, quantity)
        return redirect('cart:cart_detail')


def cart_detail(request):
    """展示 cart"""
    cart = Cart(request)
    now = timezone.now()
    if request.method == 'POST':
        coupon_form = CouponForm(request.POST)
        if coupon_form.is_valid():
            code = coupon_form.cleaned_data['code']
            try:
                coupon = get_object_or_404(Coupon,
                                           code=code,
                                           is_actived=True,
                                           valid_from__lt=now,
                                           valid_to__gt=now,
                                           )
            except Http404:
                messages.warning(request, f"优惠劵代码错误/已过期/已失效")
    else:
        coupon_form = CouponForm()
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'coupon_form': coupon_form})
