import debug_toolbar

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from barter import views
from . import settings
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('items/', views.show_all_items, name='items'),
    path('', views.index, name='home'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.SignupUserView.as_view(), name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
