from collections import OrderedDict

from redis import StrictRedis

from django_blog import settings
from shop.models import Product

r = StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class Recommender(object):
    def get_product_key(self, id):
        """
        Redis 中 product 的 id,准确说是 key
        """
        return f"product:{id}:with"

    def cal_products_bought(self, products):
        """计算同一 order 内所有 product 的 score """
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    r.zincrby(self.get_product_key(product_id), with_id, amount=1)

    def get_suggest_products(self, products, max_results=4):
        """
        根据 order 给定的产品集，计算分数，返回分数最高的几个结果
        :products:order products
        :return:product_ids list

        """
        # 仅有一个产品
        if len(products) == 1:
            suggest_products = r.zrange(self.get_product_key(products[0].id),
                                        start=0, end=-1, desc=True)[:max_results]
            suggest_product_ids = [int(i) for i in suggest_products]
        else:
            product_ids = [p.id for p in products]
            score = {}
            for id in product_ids:
                with_product_scores = r.zrange(self.get_product_key(id), 0, -1, withscores=True)
                for i in with_product_scores:
                    with_product_id = int(i[0])
                    with_product_score = i[1]
                    if with_product_id in score:
                        # 如已加入，递增分数
                        score[with_product_id] += with_product_score
                    else:
                        # 如未加入，保存加入
                        score[with_product_id] = with_product_score
            order_score = OrderedDict(sorted(score.items(), key=lambda x: x[1], reverse=True))
            suggest_product_ids = [i for i in score.keys()][:max_results]
        return suggest_product_ids

    def clear(self):
        for i in Product.objects.values_list('id'):
            r.delete(self.get_product_key(id=i))
