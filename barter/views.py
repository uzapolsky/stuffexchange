from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse

from .models import Item


class LoginUserView(LoginView):
    def get_success_url(self):
        return reverse('home')


def index(request):
    return render(request, 'index.html')


def show_all_items(request):
    items = Item.objects.all()
    return render(request, 'items.html', context={'items': items})
