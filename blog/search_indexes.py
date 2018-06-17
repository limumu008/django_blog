from haystack import indexes

from blog.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    """article search index"""
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author')
    publish = indexes.DateTimeField(model_attr='publish')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.exclude(status='draft')
