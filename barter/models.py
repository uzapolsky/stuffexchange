from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.forms import ModelForm, FileField, ClearableFileInput


class Category(models.Model):
    name = models.CharField(
        'название',
        max_length=50,
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(
        'название',
        max_length=50,
    )
    description = models.TextField(
        'описание',
        blank=True,
    )

    category = models.ForeignKey(
        Category,
        verbose_name='категория',
        related_name='items',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        User,
        verbose_name='владелец',
        related_name='owned_items',
        on_delete=models.CASCADE,
    )
    wished_by = models.ManyToManyField(
        User,
        verbose_name='нужен',
        related_name='wished_items',
        blank=True,
    )
    added_at = models.DateTimeField(
        'добавлен в',
        default=timezone.now,
        db_index=True,
    )

    class Meta:
        verbose_name = 'предмет'
        verbose_name_plural = 'предметы'

    def __str__(self):
        return self.name


class Photo(models.Model):
    image = models.ImageField(
        'фото',
    )

    item = models.ForeignKey(
        Item,
        verbose_name='предмет',
        related_name='photos',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'фото'
        verbose_name_plural = 'фото'

    def __str__(self):
        return self.item.name


class AddItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'category']

class AddItemFullForm(AddItemForm):
    images = FileField(widget=ClearableFileInput(attrs={'multiple': True}))

    class Meta(AddItemForm.Meta):
        fields = AddItemForm.Meta.fields + ['images',]