from django import forms
from django.utils.translation import gettext_lazy as _
from markdownx.fields import MarkdownxFormField

from blog.models import Article, Comment


class EmailArticleForm(forms.Form):
    name = forms.CharField(max_length=200, label='你的名字(可选)', required=False)
    to = forms.EmailField(label='目标邮件')
    comment = forms.CharField(required=False, widget=forms.Textarea, label='评论')


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content': ''
        }

    def __init__(self, *args, **kwargs):
        """修改 widget 尺寸"""
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'cols': 80, 'rows': 2})


class ArticleForm(forms.ModelForm):
    error_messages = {
        'languages': _('请使用英文标签及逗号'),
    }
    content = MarkdownxFormField(label='文章内容', required=False)

    class Meta:
        model = Article
        fields = ['title', 'content', 'status', 'tags']
        labels = {
            'title': '文章标题',
            'status': '文章状态',
            'tags': '文章标签',
        }
        help_texts = {
            'tags': '使用英文标签，使用逗号分隔'
        }

    def __init__(self, *args, **kwargs):
        """修改 widget 尺寸"""
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'cols': 64, 'rows': 15})

    def clean_tags(self):
        """限制仅使用英文标签"""
        tags = self.cleaned_data['tags']
        for tag in tags:
            for char in tag:
                if ('\u0041' <= char <= '\u005a') or ('\u0061' <= char <= '\u007a'):
                    pass
                else:
                    raise forms.ValidationError(
                            self.error_messages['languages'],
                            code='languages',
                    )
        else:
            return tags
