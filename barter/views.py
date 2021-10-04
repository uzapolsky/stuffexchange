from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.template.context_processors import csrf
from django.urls import reverse
from django.views import View

from .forms import AddItemFullForm, CategoryForm, UserCreationWithEmailForm
from .models import Item, Photo, Wish, User


class LoginUserView(LoginView):
    def get_success_url(self):
        return reverse('home')


class SignupUserView(View):

    def get(self, request):
        form = UserCreationWithEmailForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationWithEmailForm(request.POST)
        if not form.is_valid():
            return render(request, 'registration/signup.html', {'form': form})
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')


class AddItemView(View):

    def get(self, request):
        form = AddItemFullForm()
        return render(request, 'add-item.html', {'form': form})

    def post(self, request):
        form = AddItemFullForm(request.POST, request.FILES or None)
        images = request.FILES.getlist('images')

        if not form.is_valid():
            messages.error(request, form.errors.get('description', 'Ошибка'))
            return redirect('add-item')
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
        messages.success(request, f'{item.name} успешно добавлен')
        return redirect('user-items', user.id)


def index(request):
    return redirect('items')


def handle_category_form(request, items):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if not form.is_valid():
            messages.error(request, form.errors.get('description', 'Ошибка'))
            context = {'items': items, 'form': form}
            return render(request, 'items.html', context=context)
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
    items = (
        Item.objects
        .select_related('category')
        .order_by('name')
        .exclude(owner=user)
        .order_by('id')
    )

    context = handle_category_form(request, items)
    return render(request, 'items.html', context=context)


def show_user_items(request, user_id):
    items = Item.objects.filter(owner=user_id).select_related('category').order_by('-id')
    context = handle_category_form(request, items)
    context['site_user'] = get_object_or_404(User, pk=user_id)
    return render(request, 'user-items.html', context=context)


def show_item(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'show-item.html', context={'item': item})


def show_offers(request):
    user = request.user.id
    items = Item.objects.filter(owner=user).prefetch_related('wished_by', 'category')
    item_users = [(item, item.wished_by.all()) for item in items if item.wished_by.all().exists()]

    wanted_items = []
    for item, users in item_users:
        for user in users:
            wish_time = item.wish.first().wished_at.strftime('%d.%m.%Y %H:%M')
            print(type(wish_time))
            wanted_items.append((item, user, wish_time))

    return render(request, 'offers.html', context={'wanted_items': wanted_items})


def offer_exchange(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item.wished_by.add(request.user.id)
    messages.success(request, f'Уведомление о желании об {item.name} отправлено')
    return redirect('items')


def delete_offer(request, item_id, wisher_id):
    wish = get_object_or_404(Wish, item=item_id, wisher=wisher_id)
    wish.delete()
    messages.success(request, 'Удаление успешно')
    return redirect('offers')


def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item.delete()
    messages.success(request, 'Предмет удален')
    return redirect('user-items', request.user.id)
