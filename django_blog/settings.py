import os

from django.urls import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open('django_blog/key.txt') as f:
    SECRET_KEY = f.read().strip()

DEBUG = True

ALLOWED_HOSTS = ['localhost', 'qinglanjun.com', '.qinglanjun.com']

INSTALLED_APPS = [
    'account.apps.AccountConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'haystack',
    'django.forms',
    'blog.apps.BlogConfig',
    'taggit',
    'markdownx',
    'gunicorn',
    'avatar',
    'actions.apps.ActionsConfig',
    'shop.apps.ShopConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

WSGI_APPLICATION = 'django_blog.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'host': 'localhost',
        'TIME_ZONE': 'Asia/Shanghai',
        'OPTIONS': {
            'read_default_file': 'C:\ProgramData\MySQL\MySQL Server 5.7\my.ini',
            'isolation_level': 'read committed',
            'init_command': 'SET default_storage_engine=INNODB',
        }
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# auth
AUTH_USER_MODEL = 'account.User'
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
PASSWORD_RESET_DAYS = 3
LOGOUT_REDIRECT_URL = None
LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('account:profile')

ABSOLUTE_URL_OVERRIDES = {
    'account.user': lambda u: reverse_lazy('account:user_detail',
                                           kwargs={'username': u.username})
}

# email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SUBJECT_PREFIX = '[Django] '
EMAIL_USE_LOCALTIME = False
EMAIL_USE_TLS = False
EMAIL_PORT = 465
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = 'wangzhou8284@163.com'
EMAIL_HOST = 'smtp.163.com'
EMAIL_HOST_USER = 'wangzhou8284@163.com'
EMAIL_HOST_PASSWORD = 'wyyxsq522421519'

# safe
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
# SECURE_SSL_REDIRECT = True

# markdown
MARKDOWNX_MARKDOWN_EXTENSIONS = ['markdown.extensions.extra',
                                 'markdown.extensions.codehilite',
                                 'markdown.extensions.toc']

# search:haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.join(BASE_DIR, 'whoosh_index')),
    },
}
# 每页结果
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
