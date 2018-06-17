from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

from cart.cart import Cart
from coupons.forms import CouponForm
from shop.models import Product
from shop.recommender import Recommender


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
        if cart.coupon:
            discount = cart.coupon.discount
        else:
            discount = 0
        return JsonResponse(
            {'status': 'rm_success',
             'this_price': this_price,
             'discount': discount}
        )
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
    coupon_form = CouponForm()
    # 推荐
    recommender = Recommender()
    cart_products = [item['product'] for item in cart]
    suggest_product_ids = recommender.get_suggest_products(cart_products)
    if not suggest_product_ids:
        suggest_products = None
    else:
        suggest_products = Product.objects.filter(pk__in=suggest_product_ids, is_sold=True)
    return render(request, 'cart/cart_detail.html', locals())
