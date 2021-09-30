from django.contrib import admin
from django.contrib.auth.models import User
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Category, Item, Photo


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class ItemResource(resources.ModelResource):
    class Meta:
        model = Item


admin.site.unregister(User)

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
    inlines = (PhotoInline,)
    raw_id_fields = ('wished_by',)
    resource_class = ItemResource


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
