from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm


def register(request):
    form = UserCreationForm()
    return render(request, 'login/register.html', {'form': form})


def sign_in(request):
    return render(request, 'login/sign_in.html')


def dashboard(request):
    return render(request, 'login/dashboard.html')