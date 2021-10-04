# Generated by Django 3.2.7 on 2021-10-04 10:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0002_user_contacts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='contacts',
            field=models.TextField(blank=True, validators=[django.core.validators.MaxLengthValidator(200)], verbose_name='контакты'),
        ),
    ]
