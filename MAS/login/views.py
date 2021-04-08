from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def register(request):
    form = UserCreationForm()
    return render(request, 'login/register.html', {'form': form})


def sign_in(request):
    return render(request, 'login/sign_in.html')


@login_required
def dashboard(request):
    return render(request, 'login/dashboard.html')


def logout_view(request):
    logout(request)

