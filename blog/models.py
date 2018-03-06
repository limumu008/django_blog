from django.conf import settings
from django.db import models
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
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='draft', choices=STATUS_CHOICES)

    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:articles', kwargs={'pk': self.pk})


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.TextField()
    is_show = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f"{self.content}"
