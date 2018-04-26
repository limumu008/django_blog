from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse, Http404
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)
from django.views import generic
from django.views.decorators.http import require_POST
from taggit.models import Tag

from actions.utils import create_action
from blog.search_indexes import ArticleIndex
from blog.utils import toggle_pages, create_like
from .forms import (ArticleCommentForm, ArticleForm, EmailArticleForm, ReplyForm)
from .models import Article, Reply, Comment


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
        page_toggle = toggle_pages(context['articles'])
        context['page_toggle'] = page_toggle
        try:
            context['tag'] = self.tag
            return context
        except AttributeError:
            context['latest_articles'] = Article.published.order_by('-created')[:5]

            context['random_articles'] = Article.published.order_by('?')[:5]

            return context


class MyArticles(LoginRequiredMixin, IndexView):
    template_name = 'blog/my_articles.html'
    context_object_name = 'articles'

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
    context_object_name = 'articles'

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
        if article.author.profile.is_author:
            article.save()
            # 重建索引
            article_index = ArticleIndex()
            article_index.reindex()
            create_action(article.author, article,
                          f"{article.author.username} 发表了文章《{article.title}》")
            return super().form_valid(form)
        else:
            raise Http404("你不是作者，不能发表文章")


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
    # 用户是否登录的变量，用于 js
    if request.user.is_authenticated:
        user_logined = 'yes'
    else:
        user_logined = 'no'
    # 检索相似
    article_id_list = article.tags.values_list('id', flat=True)
    similar_articles = Article.published.filter(
        tags__in=article_id_list). \
        exclude(id=article.id)
    similar_articles = similar_articles.annotate(
        same_tags=Count('tags')).order_by('-same_tags', '-created')[:5]
    # 检索随机
    random_articles = Article.published.order_by('?').exclude(id=article.id)[:5]
    # 检索评论
    comments_list = article.comments.filter(is_show=True).select_related('author'). \
        prefetch_related('replies__author', 'replies__reply_target')
    # 评论分页
    page_toggle = toggle_pages(comments_list)
    paginator = Paginator(comments_list, 10)
    page = request.GET.get('page')
    comments = paginator.get_page(page)
    # 添加阅读次数
    article.add_read_times()
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
            return redirect(article)
    else:
        comment_form = ArticleCommentForm()
    context = {'article': article,
               'comments': comments,
               'comment_form': comment_form,
               'article_author': article_author,
               'similar_articles': similar_articles,
               'random_articles': random_articles,
               'user_logined': user_logined,
               'page_toggle': page_toggle,
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


@login_required
def user_like(request):
    """用户给文章/评论/回复点赞"""
    if request.POST.get('target') == 'article':
        article_id = request.POST.get('article_id')
        target = get_object_or_404(Article, pk=article_id)
        # 用户点/取消赞
    elif request.POST.get('target') == 'comment':
        comment_id = request.POST.get('comment_id')
        target = get_object_or_404(Comment, pk=comment_id)
        # 用户点/取消赞
    elif request.POST.get('target') == 'reply':
        reply_id = request.POST.get('reply_id')
        target = get_object_or_404(Reply, pk=reply_id)
        # 用户点/取消赞
    like = create_like(request.user, target)
    is_liked = like.is_liked
    return JsonResponse({'status': is_liked})


@require_POST
def reply(request):
    """回复评论"""
    reply_form = ReplyForm(request.POST)
    action = request.POST.get('action')
    # 新回复
    if reply_form.is_valid():
        # 使用 content
        new_reply = reply_form.save(commit=False)
        # author
        new_reply.author = request.user
        if action == 'reply_comment':
            # 已获得 comment_id
            new_reply.comment = get_object_or_404(Comment, id=request.POST.get('comment'))
            new_reply.reply_target = new_reply.comment.author
            new_reply.save()
            create_action(user=request.user,
                          target=new_reply.comment,
                          verb=f"{request.user.username} 回复了评论 '{new_reply}'")
            reply_content = \
                rf"<div class='replies'>" \
                rf"<p><span class='temp_reply'>{request.user.username}</span> : {new_reply}</p>" \
                rf"<p class='extra_info'>{new_reply.created:%y/%m/%d %H:%M}</p>" \
                rf"</div>"
            return JsonResponse({'status': 'reply_ok',
                                 'reply_text': reply_content})

        elif action == 'reply_reply':
            # 未获得 comment，获得 reply
            selected_reply_id = request.POST.get('selected_reply')
            selected_reply = get_object_or_404(Reply, id=selected_reply_id)
            new_reply.comment = selected_reply.comment
            comment_id = new_reply.comment.id
            new_reply.reply_target = selected_reply.author
            new_reply.save()
            create_action(user=request.user,
                          target=new_reply.reply_target,
                          verb=f"{request.user.username} 回复了 '{new_reply.reply_target.username}'")
            reply_content = \
                rf"<div class='replies'>" \
                rf"<p><span class='temp_reply'>{request.user.username}</span> @ " \
                rf"<span class='temp_reply'>{new_reply.reply_target.username}</span> : {new_reply}" \
                rf"<p class='extra_info'>{new_reply.created:%y/%m/%d %H:%M}</p>" \
                rf"</div>"
            return JsonResponse({'status': 'reply_ok',
                                 'comment_id': comment_id,
                                 'reply_text': reply_content})
