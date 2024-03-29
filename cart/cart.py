from decimal import Decimal

from coupons.models import Coupon
from django_blog import settings
from shop.models import Product


class Cart:
    def __init__(self, request):
        """初始化"""
        self.session = request.session
        # 这里拿到了 sessions 中的 cart，不存在就设为 {}
        self.cart = self.session.setdefault(settings.CART_SESSION_ID, {})
        self.coupon_id = self.session.get('coupon_id')

    def __str__(self):
        return str(self.cart)

    def add(self, product, quantity=1):
        """
        添加 product 到 cart,已存在则+1
        :param product:shop:product
        :param quantity:int:for product
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def change(self, product, quantity):
        """修改 cart 中 product 的 quantity"""
        product_id = str(product.id)
        self.cart[product_id]['quantity'] = quantity
        self.save()

    def remove(self, product):
        """remove a product form cart"""
        product_id = str(product.id)
        del self.cart[product_id]
        self.save()

    def clear(self):
        """remove cart from session"""
        del self.session[settings.CART_SESSION_ID]
        try:
            del self.session['coupon_id']
        except KeyError:
            pass

    def save(self):
        """update session"""
        self.session.modified = True

    def __iter__(self):
        """
        迭代产出 product
        另：将 price 转换 Decimal
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        # 向 cart 中 product 对应 id 的 value 中添加 product实例：product/price/quantity
        for product in products:
            self.cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            # item 是 dict
            # 将 price str convert to Decimal
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            # item:{'product':product,'price':price,'quantity':quantity,'total_price':total_price}
            yield item

    def __len__(self):
        """cal all products in cart"""
        return sum(item['quantity'] for item in self.cart.values())

    def __getitem__(self, item):
        return self.cart[item]

    def get_total_price(self):
        return sum(item['total_price'] for item in self.cart.values())

    # 优惠劵
    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            return self.get_total_price() * self.coupon.discount / 100
        else:
            return Decimal('0')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
