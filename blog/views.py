from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .forms import EmailArticleForm
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


def share_article(request, id):
    article = get_object_or_404(Article, id=id)
    cd = None
    is_sent = False
    if request.method == "POST":
        form = EmailArticleForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            article_url = request.build_absolute_uri(article.get_absolute_url())
            subject = f"{cd['name']}({cd['email']}) 建议你读一下《{article.title}》"
            message = f"{article_url} " \
                      f"{cd['name']}的评论：{cd['comment']}"
            send_mail(subject, message, 'wangzhou8284@163.com', [cd['to']])
            is_sent = True
    else:
        form = EmailArticleForm()
    context = {'article': article, 'cd': cd, 'form': form, 'is_sent': is_sent}
    return render(request, 'blog/share_article.html', context)

