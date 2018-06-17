from haystack import indexes

from shop.models import Product


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    """product search index"""
    text = indexes.CharField(document=True, use_template=True)
    category = indexes.CharField(model_attr='category')

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        return self.get_model().objects.exclude(is_sold=False)
