from django.contrib import admin

from .models import Item, Photo, Category


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
