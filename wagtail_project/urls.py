from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from search import views as search_views

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
]

urlpatterns += i18n_patterns(
    path('', include(wagtail_urls)),
    path("search/", search_views.search, name="search"),
)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
