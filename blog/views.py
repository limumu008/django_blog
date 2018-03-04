from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .forms import ArticleCommentForm, EmailArticleForm
from .models import Article


class IndexView(generic.ListView):
    queryset = Article.published.all()
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    paginate_by = 10


def article_detail(request, pk):
    article = get_object_or_404(Article, id=pk)
    comments = article.comments.filter(is_show=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = ArticleCommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.article = article
            new_comment.save()
    else:
        comment_form = ArticleCommentForm()
    context = {'article': article,
               'comments': comments,
               'comment_form': comment_form,
               'new_comment': new_comment}
    return render(request, 'blog/article.html', context)


def share_article(request, id):
    article = get_object_or_404(Article, id=id)
    cd = None
    is_sent = False
    if request.method == "POST":
        form = EmailArticleForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            article_url = request.build_absolute_uri(article.get_absolute_url())
            subject = f"{cd['name']} 建议你读一下《{article.title}》"
            message = f"{article_url} " \
                      f"{cd['name']}的评论：{cd['comment']}"
            send_mail(subject, message, 'wangzhou8284@163.com', [cd['to']])
            is_sent = True
    else:
        form = EmailArticleForm()
    context = {'article': article, 'cd': cd, 'form': form, 'is_sent': is_sent}
    return render(request, 'blog/share_article.html', context)
