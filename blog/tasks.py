from django.core.mail import send_mail

from blog.models import Article
from django_blog.celery import app


@app.task
def article_shared(url, cd, article_id):
    """send mail,return the result:1/0"""
    article = Article.objects.get(id=article_id)
    subject = f"{cd['name']} 建议你读一下《{article.title}》"
    message = f"{url} " \
              f"{cd['name']}的评论：{cd['comment']}"
    mail_sent = send_mail(subject, message, 'wangzhou8284@163.com', [cd['to']])
    return mail_sent
