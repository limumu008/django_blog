from django.views import generic

from .models import Article


class IndexView(generic.ListView):
    queryset = Article.published.all()
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    paginate_by = 10


class ArticleView(generic.DetailView):
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'
