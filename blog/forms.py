from django import forms

from blog.models import Comment


class EmailArticleForm(forms.Form):
    name = forms.CharField(max_length=200, label='你的名字')
    to = forms.EmailField(label='目标邮件')
    comment = forms.CharField(required=False, widget=forms.Textarea, label='评论')


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content': ''
        }
