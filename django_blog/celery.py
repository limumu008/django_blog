from __future__ import absolute_import

import os

from celery import Celery

# 防止 celery.py 和 celery 库冲突

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')

app = Celery('django_blog')

app.config_from_object('django.conf:settings', namespace='CELERY')

# auto find task from installed apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request:{self.request!r}")
