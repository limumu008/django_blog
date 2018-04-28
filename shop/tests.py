from django.test import TestCase
from django.urls import reverse

from shop.models import Category


class TestProductList(TestCase):
    def test_product_list(self):
        r = self.client.get(reverse('shop:product_list'))
        # 页面正常运行
        self.assertEqual(r.status_code, 200)
        # 模板正常使用
        self.assertTemplateUsed(r, 'shop/product/list.html')

    def test_category(self):
        category_fruit = Category.objects.create(name='fruit', slug='fruit')
        r = self.client.get(reverse('shop:category_product_list', kwargs={'category_slug': category_fruit.slug}))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, 'shop/product/list.html')
