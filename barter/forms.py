from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, FileField, ClearableFileInput

from .models import Item, Category, User


class AddItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'category']


class AddItemFullForm(AddItemForm):
    images = FileField(widget=ClearableFileInput(attrs={'multiple': True}))

    class Meta(AddItemForm.Meta):
        fields = AddItemForm.Meta.fields + ['images']


class CategoryForm(forms.Form):
    category_choices = [(0, 'категории'), (0, 'все категории')]
    category_choices.extend(Category.objects.values_list('id', 'name'))
    category = forms.ChoiceField(
        label='days',
        choices=category_choices,
        required=False,
        initial='0',
    )


class UserCreationWithEmailForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'contacts', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreationWithEmailForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Юзернейм"
        self.fields['username'].help_text = "Обязательное поле. Только английские буквы, цифры и символы @/./+/-/_"
        self.fields['email'].label = "Почта"
        self.fields['password1'].label = "Пароль"
        self.fields['password1'].help_text = "8 символов, не только цифры, не должен совпадать с другими полями"
        self.fields['password2'].label = "Подтверждение пароля"
        self.fields['password2'].help_text = "Должен точно совпадать с паролем"
