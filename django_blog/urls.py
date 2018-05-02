from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from django_blog import settings

urlpatterns = [
                  path('', TemplateView.as_view(template_name='index.html'), name='index'),
                  path('account/', include('account.urls')),
                  path('account/', include('django.contrib.auth.urls')),
                  path('blog/', include('blog.urls')),
                  path('shop/', include('shop.urls')),
                  path('cart/', include('cart.urls')),
                  path('admin/', admin.site.urls),
                  path(r'markdownx/', include('markdownx.urls')),
                  path(r'search/', include('haystack.urls')),
                  path(r'avatar/', include('avatar.urls'), )] + static(settings.STATIC_URL,
                                                                       document_root=settings.STATIC_ROOT) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
