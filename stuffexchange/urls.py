import debug_toolbar
from barter import views
from barter.forms import UserLoginForm
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('items/', views.show_all_items, name='items'),
    path('user/<int:user_id>', views.show_user_items, name='user-items'),
    path('', views.index, name='home'),
    path('login/', views.LoginUserView.as_view(authentication_form=UserLoginForm), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.SignupUserView.as_view(), name='signup'),
    path('add-item/', views.AddItemView.as_view(), name='add-item'),
    path('item/<int:item_id>', views.show_item, name='show_item'),
    path('offers/', views.show_offers, name='offers'),
    path('exchange/<int:item_id>', views.offer_exchange, name='exchange'),
    path('delete_wish/<int:item_id>/<int:wisher_id>', views.delete_offer, name='delete_offer'),
    path('delete_item/<int:item_id>', views.delete_item, name='delete_item'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
