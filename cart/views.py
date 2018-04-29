from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from cart.cart import Cart
from shop.models import Product


@require_POST
def change_cart(request):
    """
    根据 post 的 action 选择行动：增加/减少/移除 product，或者 clear cart。
    根据 post 的 product_id 选择操作的 product。
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=request.POST.get('product_id'))
    if request.POST.get('action') == 'add_product':
        cart.add(product)
        return JsonResponse({'status': 'add_success'})
    elif request.POST.get('action') == 'reduce_product':
        cart.reduce(product)
    elif request.POST.get('action') == 'remove_product':
        cart.remove(product)
    elif request.POST.get('action') == 'clear_cart':
        cart.clear()


def cart_detail(request):
    """展示 cart"""
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})
