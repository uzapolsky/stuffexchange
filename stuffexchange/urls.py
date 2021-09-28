from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from barter import views
from . import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/', views.show_all_items, name='post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)