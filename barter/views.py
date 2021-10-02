from itertools import zip_longest

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.template.context_processors import csrf
from django.urls import reverse
from django.views import View

from .forms import AddItemFullForm, CategoryForm
from .models import Item, Photo


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
                category=category,
            )
            for image in images:
                Photo.objects.create(item=item, image=image)
            return redirect('user-items')
        else:
            print("Form invalid")
            return redirect('add-item')


def index(request):
    return redirect('items')


def handle_category_form(request, items):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if not form.is_valid():
            context = {'items': items, 'form': form}
            return render(request, 'items.html')
        if int(category_id := request.POST.get('categories')):
            items = items.filter(category=category_id)
    else:
        form = CategoryForm()
    items = pagination(request, items)
    context = {'items': items, 'form': form}
    context.update(csrf(request))
    return context


def pagination(request, items, items_per_page=6):
    paginator = Paginator(items, items_per_page)
    page = request.GET.get('page')
    return paginator.get_page(page)


def show_all_items(request):
    user = request.user.id
    items = Item.objects.select_related('category').order_by('name').exclude(owner=user)

    context = handle_category_form(request, items)
    return render(request, 'items.html', context=context)


def show_my_items(request, user_id):
    user = request.user.id
    items = Item.objects.filter(owner=user_id).select_related('category')
    context = handle_category_form(request, items)
    return render(request, 'user-items.html', context=context)


def show_item(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'show-item.html', context={'item': item})


def show_offers(request):
    user = request.user.id
    items = Item.objects.filter(owner=user).prefetch_related('wished_by', 'category')
    item_users = [(item, item.wished_by.all()) for item in items if item.wished_by.all().exists()]

    wanted_items = list()
    for item, users in item_users:
        for user in users:
            wanted_items.append((item, user))

    return render(request, 'offers.html', context={'wanted_items': wanted_items})


def offer_exchange(request, item_id):
    return render(request, 'exchange.html')
