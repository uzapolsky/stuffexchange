from django import forms

from django.forms import ModelForm, FileField, ClearableFileInput
from .models import Item, Category


class AddItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'category']


class AddItemFullForm(AddItemForm):
    images = FileField(widget=ClearableFileInput(attrs={'multiple': True}))

    class Meta(AddItemForm.Meta):
        fields = AddItemForm.Meta.fields + ['images',]


class CategoryForm(forms.Form):
    category = forms.ChoiceField(
        label='days',
        choices=tuple(Category.objects.values_list('id', 'name')),
        required=False,
    )
