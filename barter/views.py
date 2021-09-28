from django.shortcuts import render
from .models import Item


def show_all_items(request):
    items = Item.objects.all()
    return render(request, 'index.html', context={'items': items})
