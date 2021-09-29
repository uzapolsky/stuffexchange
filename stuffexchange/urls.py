import debug_toolbar

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from barter import views
from . import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/', views.show_all_items, name='post'),
    path('', views.index, name='/'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),