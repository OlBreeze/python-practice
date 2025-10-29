from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegistrationForm, UserProfileForm, PasswordChangeForm
from .models import UserProfile


def register_view(request):
    """Представлення для реєстрації нових користувачів"""
    if request.user.is_authenticated:
        return redirect('profile', username=request.user.username)

    if request.method == 'POST':  # Если GET —
        # значит, просто открыл страницу регистрации (нужно показать пустую форму)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вітаємо! Ви успішно зареєструвалися.')
            return redirect('profile', username=user.username)
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def edit_profile_view(request):
    """Представлення для редагування профілю користувача"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профіль успішно оновлено.')
            return redirect('profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def change_password_view(request):
    """Представлення для зміни паролю користувача"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # Оновлюємо сесію, щоб користувач залишився авторизованим
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Ваш пароль успішно змінено.')
            return redirect('profile', username=request.user.username)
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def profile_view(request, username):
    """Представлення для перегляду профілю користувача"""
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=user)

    context = {
        'profile_user': user,
        'profile': profile,
        'is_own_profile': request.user == user
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def delete_account_view(request):
    """Представлення для видалення облікового запису (додаткова функція)"""

    # Заборонити видалення суперкористувачів
    if request.user.is_superuser:
        messages.error(request, 'Неможливо видалити обліковий запис суперкористувача.')
        return redirect('profile', username=request.user.username)

    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Ваш обліковий запис успішно видалено.')
        return redirect('register')

    return render(request, 'accounts/delete_account.html')


@login_required
def users_list_view(request):
    """Представлення для перегляду списку всіх користувачів"""
    from django.core.paginator import Paginator

    # Отримання всіх користувачів з профілями
    users = User.objects.select_related('profile').all().order_by('-date_joined')

    # Пагінація (3 користува на сторінку)
    paginator = Paginator(users, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_users': users.count()
    }

    return render(request, 'accounts/users_list.html', context)

def logout_view(request):
    """Представлення для виходу з системи (підтримує GET і POST)"""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'Ви успішно вийшли з системи.')
    return redirect('login')