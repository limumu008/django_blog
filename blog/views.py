from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)
from django.urls import reverse
from django.views import generic
from taggit.models import Tag

from actions.utils import create_action
from blog.utils import create_like_article
from .forms import (ArticleCommentForm, ArticleForm, EmailArticleForm)
from .models import Article, Likes


class IndexView(generic.ListView):
    """文章展示页"""
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        try:
            tag_slug = self.kwargs['tag_slug']
            tag = get_object_or_404(Tag, slug=tag_slug)
            self.tag = tag
            return Article.published.filter(tags__name__in=[tag]).order_by('-publish')
        except KeyError:
            return Article.published.order_by('-publish')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['tag'] = self.tag
            return context
        except AttributeError:
            context['latest_articles'] = Article.published.order_by('-created')[:5]

            context['random_articles'] = Article.published.order_by('?')[:5]

            return context


class MyArticles(LoginRequiredMixin, IndexView):
    template_name = 'blog/my_articles.html'
    context_object_name = 'my_articles'

    def get_queryset(self):
        try:
            tag_slug = self.kwargs['tag_slug']
            tag = get_object_or_404(Tag, slug=tag_slug)
            self.tag = tag
            return Article.published.filter(tags__name__in=[tag]). \
                filter(author=self.request.user).order_by('-publish')
        except KeyError:
            return Article.published.filter(author=self.request.user)


class MyDrafts(LoginRequiredMixin, IndexView):
    template_name = 'blog/my_drafts.html'
    context_object_name = 'my_drafts'

    def get_queryset(self):
        try:
            tag_slug = self.kwargs['tag_slug']
            tag = get_object_or_404(Tag, slug=tag_slug)
            self.tag = tag
            return Article.objects.filter(tags__name__in=[tag]). \
                filter(status='draft'). \
                filter(author=self.request.user).order_by('-publish')
        except KeyError:
            return Article.objects.filter(author=self.request.user). \
                filter(status='draft')


def archives(request):
    """文章归档"""
    archives = []
    dates = Article.published.dates('publish', 'month', order='DESC')
    for date in dates:
        year = date.year
        month = date.month

        if month < 10:
            month_str = str(year) + '-0' + str(month)
        else:
            month_str = str(year) + '-' + str(month)
        articles = Article.published.filter(
                publish__startswith=month_str).order_by('-publish')
        archives.append(articles)
    date_archives = zip(dates, archives)
    context = {'date_archives': date_archives}
    return render(request, 'blog/article_archives.html', context)


class NewArticle(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/new_article.html'
    success_message = '发表成功'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        create_action(article.author, article,
                      f"{article.author.username} 发表了文章《{article.title}》")
        return super().form_valid(form)


class UpdateArticle(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/update_article.html'
    success_message = '修改成功'

    def form_valid(self, form):
        article = form.save(commit=False)
        author = self.request.user
        article.save()
        create_action(article.author, article,
                      f"{author.username} 修改了文章《{article.title}》")
        return super().form_valid(form)


def article_detail(request, pk):
    article = get_object_or_404(Article, id=pk)
    # 添加阅读次数
    article.add_read_times()
    # 检索相似
    article_id_list = article.tags.values_list('id', flat=True)
    similar_articles = Article.published.filter(
            tags__in=article_id_list). \
        exclude(id=article.id)
    similar_articles = similar_articles.annotate(
            same_tags=Count('tags')).order_by('-same_tags', '-created')[:5]
    # 检索随机
    random_articles = Article.published.order_by('?').exclude(id=article.id)[:5]
    comments = article.comments.filter(is_show=True)
    # 判断是否文章作者，以决定是否显示修改文章按钮。
    article_author = False
    if request.user.is_authenticated:
        user = request.user
        if article.author == user:
            article_author = True
    # 评论
    if request.method == 'POST':
        if request.user.is_anonymous:
            # 如未登录重定向到登录
            return redirect('login')
        comment_form = ArticleCommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.article = article
            new_comment.save()
            create_action(request.user, article,
                          verb=f"{request.user.username} 评论了文章《{article.title}》")
            messages.success(request, '评论成功')
    else:
        comment_form = ArticleCommentForm()
    # 控制赞开关的变量
    try:
        content_type = ContentType.objects.get_for_model(article)
        like = Likes.objects.get(user=request.user,
                                 content_type=content_type,
                                 object_id=article.id)
        is_liked = like.is_liked
    except Exception as e:
        is_liked = False
    context = {'article': article,
               'comments': comments,
               'comment_form': comment_form,
               'author_author': article_author,
               'similar_articles': similar_articles,
               'random_articles': random_articles,
               'is_liked': is_liked,
               }
    return render(request, 'blog/article.html', context)


def share_article(request, id):
    """通过邮件分享文章"""
    article = get_object_or_404(Article, id=id)
    cd = None
    if request.method == "POST":
        form = EmailArticleForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            article_url = request.build_absolute_uri(article.get_absolute_url())
            subject = f"{cd['name']} 建议你读一下《{article.title}》"
            message = f"{article_url} " \
                      f"{cd['name']}的评论：{cd['comment']}"
            send_mail(subject, message, 'wangzhou8284@163.com', [cd['to']])
            create_action(request.user, article,
                          verb=f"{request.user.username} 分享了文章《{article.title}》")
            messages.success(request, '分享成功')
            return redirect(article)
    else:
        form = EmailArticleForm()
    context = {'article': article,
               'cd': cd, 'form': form,
               }
    return render(request, 'blog/share_article.html', context)


def retrieve_tags(request):
    """显示全部标签(可链接文章)"""
    articles = Article.published.all()
    tags = []
    for article in articles:
        for tag in article.tags.all():
            if tag not in tags:
                tags.append(tag)
    return render(request, 'blog/retrieve_tags.html', {'tags': tags})


def user_like(request):
    """用户给文章或评论点赞"""
    # 用户未登录，重定向
    if request.user.is_anonymous:
        return JsonResponse({'status': 'redirect',
                             'url': reverse('login')
                             })
    # 用户登录
    article_id = int(request.POST.get('article_id'))
    article = get_object_or_404(Article, pk=article_id)
    # 用户点/取消赞
    like = create_like_article(request.user, article)
    is_liked = like.is_liked
    return JsonResponse({'status': is_liked})
