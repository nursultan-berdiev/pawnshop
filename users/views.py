from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, OfficerUpdateForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}!')
            return redirect('products')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
        'title': 'Регистрация нового пользователя'
    }
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        o_form = OfficerUpdateForm(request.POST, instance=request.user.officer)
        if u_form.is_valid() and o_form.is_valid():
            u_form.save()
            o_form.save()
            messages.success(request, f'Аккаунт изменен')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        o_form = OfficerUpdateForm(instance=request.user.officer)
    context = {
        'u_form': u_form,
        'o_form': o_form,
        'title': 'Профиль пользователя'
    }
    return render(request, 'users/profile.html', context)
