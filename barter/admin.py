from django.contrib import admin
from django.contrib.auth.models import User
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Category, Item, Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    max_num = 5


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = (PhotoInline,)
    raw_id_fields = ('wished_by',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class UserResource(resources.ModelResource):

    class Meta:
        model = User


admin.site.unregister(User)
@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource