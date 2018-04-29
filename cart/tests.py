from django.test import TestCase
from django.urls import reverse

from shop.models import Category, Product


class TestChangeCart(TestCase):
    def test_change_cart(self):
        category = Category.objects.create(name='t', slug='t')
        product = Product.objects.create(name='a', slug='a', category=category, price=5, stock=5)
        r = self.client.post(reverse('cart:change_cart'), {'action': 'add_product', 'product_id': product.id})
        self.assertEqual(r.status_code, 200)
