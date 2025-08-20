from django.shortcuts import render, redirect
from accounts.forms.CustomUserRegisterForm import CustomUserRegisterForm
from accounts.forms.CustomLoginForm import CustomLoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def signin(request):
    if request.user.is_authenticated:
        return redirect('shop:index')
    if request.method == 'POST':
        form = CustomLoginForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Your are successfully logged in !')
                return redirect('shop:index')
            else:
                messages.success(request, 'Incorrect username or password')
        else:
            messages.success(request, 'Please correct your username or password')    
                
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/signin.html', {'form': form})


def signup(request):
    if request.user.is_authenticated:
        return redirect('shop:index')
    if request.method == "POST":
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You are successful connected')
            return redirect('accounts:signin')
    else:
        form = CustomUserRegisterForm()
    return render(request, 'accounts/signup.html', {'form': form})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('shop:index')
    else :
        return redirect('accounts:signin')
            