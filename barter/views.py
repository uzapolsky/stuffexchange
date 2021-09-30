from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .models import Category, Item, Photo
from .forms import AddItemFullForm


class LoginUserView(LoginView):
    def get_success_url(self):
        return reverse('home')


class SignupUserView(View):

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        return render(request, 'registration/signup.html', {'form': form})


class AddItemView(View):

    def get(self, request):
        form = AddItemFullForm()
        return render(request, 'add-item.html', {'form': form})

    def post(self, request):
        form = AddItemFullForm(request.POST, request.FILES or None)
        print(form.errors)
        images = request.FILES.getlist('images')
        print(images, type(images))
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            item = Item.objects.create(
                owner=user,
                name=name,
                description=description,
                category=category
            )
            for image in images:
                Photo.objects.create(item=item,image=image)
            return redirect('user-items')
        else:
            print("Form invalid")
            return redirect('add-item')


def index(request):
    return render(request, 'index.html')


def show_all_items(request):
    items = Item.objects.all()
    categories = Category.objects.all()
    return render(request, 'items.html', context={'items': items, 'categories': categories})


def show_my_items(request):
    user = request.user.id
    items = Item.objects.filter(owner=user)
    categories = Category.objects.all()
    return render(request, 'user-items.html', context={'items': items, 'categories': categories})
