from django.shortcuts import render
from .models import Item


def index(request):
    return render(request, 'index.html')


def show_all_items(request):
    items = Item.objects.all()
    return render(request, 'items.html', context={'items': items})
