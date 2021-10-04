from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Category, Item, Photo, User, Wish


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class ItemResource(resources.ModelResource):
    class Meta:
        model = Item


class WishResource(resources.ModelResource):
    class Meta:
        model = Wish


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_staff')
    resource_class = UserResource


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    max_num = 5


@admin.register(Item)
class ItemAdmin(ImportExportModelAdmin):
    list_display = ('name', 'owner', 'category')
    inlines = (PhotoInline,)
    raw_id_fields = ('wished_by',)
    resource_class = ItemResource


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource


@admin.register(Wish)
class WishAdmin(ImportExportModelAdmin):
    list_display = ('item', 'wisher', 'wished_at')
    resource_class = WishResource
