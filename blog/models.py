from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'))
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='draft', choices=STATUS_CHOICES)
    read_times = models.PositiveIntegerField(default=0)

    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:articles', kwargs={'pk': self.pk})

    def add_read_times(self):
        # self.read_times += 1
        self.read_times = F('read_times') + 1
        self.save(update_fields=['read_times'])
        # 使用 F 表达式需重新从数据库加载值
        self.refresh_from_db()


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.TextField()
    is_show = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.content}"


class Likes(models.Model):
    """点赞"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='likes')
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    is_liked = models.BooleanField(default=True)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    likes_target = GenericForeignKey()

    def __str__(self):
        return f"{self.user.username}赞了{self.likes_target}"
