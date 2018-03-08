from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.views import generic
from taggit.models import Tag

from .forms import (
    ArticleCommentForm,
    EmailArticleForm,
    NewArticleForm)
from .models import Article


class IndexView(generic.ListView):
    """文章展示页"""
    queryset = Article.published.all()
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        try:
            tag_slug = self.kwargs['tag_slug']
            tag = get_object_or_404(Tag, slug=tag_slug)
            self.tag = tag
            return Article.published.filter(tags__name__in=[tag])
        except KeyError:
            return Article.published.order_by('-publish')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['tag'] = self.tag
            return context
        except AttributeError:
            return context


class NewArticle(LoginRequiredMixin, generic.CreateView):
    model = Article
    form_class = NewArticleForm
    template_name = 'blog/new_article.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        return super().form_valid(form)


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
            messages.success(request, '分享成功')

    else:
        form = EmailArticleForm()
    context = {'article': article,
               'cd': cd, 'form': form,
               'is_sent': is_sent, }
    return render(request, 'blog/share_article.html', context)


def retrieve_tags(request):
    articles = Article.published.all()
    tags = []
    for article in articles:
        for tag in article.tags.all():
            if tag not in tags:
                tags.append(tag)
    return render(request, 'blog/retrieve_tags.html', {'tags': tags})
