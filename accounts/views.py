from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserChangeForm, CustomUserCreationForm

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('mainpage:index')
    if request.method == 'POST':
        signupform = CustomUserCreationForm(request.POST)
        loginform = AuthenticationForm()
        if signupform.is_valid():
            user = signupform.save()
            auth_login(request, user)
            return redirect('mainpage:index')
    signupform = CustomUserCreationForm()
    loginform = AuthenticationForm()
    context = {
        'signupform': signupform,
        'loginform' : loginform
    }
    return render(request, 'accounts/sign.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('mainpage:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'mainpage:index')
    signupform = CustomUserCreationForm()
    loginform = AuthenticationForm()
    context = {
        'signupform': signupform,
        'loginform' : loginform
    }
    return render(request, 'accounts/sign.html', context)

def logout(request):
    auth_logout(request)
    return redirect('accounts:login')

@require_POST
def delete(request):
    request.user.delete()
    return redirect('mainpage:index')

def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            return redirect('mainpage:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)

def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:login')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/change_password.html', context)

def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    context = {
        'person': person
    }
    return render(request, 'accounts/profile.html', context)