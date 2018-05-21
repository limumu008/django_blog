from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from django_blog import settings
from order.fields import OrderField


class Subject(models.Model):
    """course 所属的主题"""
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Course(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='courses',
                                on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course:course_detail', kwargs={'pk': self.pk})


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return f"{self.order}:{self.title}"


class Content(models.Model):
    """Module 包含不同类型的文件"""
    module = models.ForeignKey(Module,
                               on_delete=models.CASCADE,
                               related_name='contents')
    content_type = models.ForeignKey(ContentType,
                                     limit_choices_to={'model_in': ('text',
                                                                    'video',
                                                                    'image',
                                                                    'file')},
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey()
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ('order',)


class ItemBase(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='%(class)s_content')
    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='course_files')


class Image(ItemBase):
    image = models.ImageField(upload_to='course_images')


class Video(ItemBase):
    """视频 url，嵌入视频"""
    url = models.URLField()
