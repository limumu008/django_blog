from django.conf import settings
from django.db import models
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'))
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='draft', choices=STATUS_CHOICES)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    # todo write get_absolute_url for model:article
