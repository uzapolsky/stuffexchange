from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .models import Item


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


def index(request):
    return render(request, 'index.html')


def show_all_items(request):
    items = Item.objects.all()
    return render(request, 'items.html', context={'items': items})
