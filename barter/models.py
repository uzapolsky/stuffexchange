from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


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
        validators=[MaxLengthValidator(1000)],
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
        through='Wish',
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


class Wish(models.Model):
    item = models.ForeignKey(
        Item,
        verbose_name='предмет',
        related_name='wish',
        on_delete=models.CASCADE,
    )
    wisher = models.ForeignKey(
        User,
        verbose_name='желающий',
        related_name='wish',
        on_delete=models.CASCADE,
    )
    wished_at = models.DateTimeField(
        'пожелали в',
        default=timezone.now,
        db_index=True,
    )


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
