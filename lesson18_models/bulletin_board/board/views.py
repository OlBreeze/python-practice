"""
Представлення (views) для застосунку дошки оголошень.

Цей модуль містить функції для відображення списків оголошень,
деталей оголошень, категорій та статистики.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.db.models import Count, Q

from .forms import AdCreateForm, AdUpdateForm, CommentForm
from .models import Ad, Category, Comment
from django.contrib import messages

def index(request: HttpRequest) -> HttpResponse:
    """
    Головна сторінка зі списком активних оголошень.

    Args:
        request: HTTP запит

    Returns:
        HttpResponse: Відрендерена сторінка
    """
    ads = Ad.objects.filter(is_active=True).select_related('category', 'user')[:10]

    context = {
        'ads': ads,
        'title': 'Головна сторінка'
    }
    return render(request, 'board/index.html', context)


def ad_list(request: HttpRequest) -> HttpResponse:
    """
    Сторінка зі списком всіх активних оголошень з можливістю фільтрації.

    Підтримує фільтрацію за:
    - категорією
    - діапазоном цін (мін/макс)
    - пошуком за заголовком

    Підтримує сортування за:
    - ціною (зростання/спадання)
    - датою створення (новіші/старіші)

    Args:
        request: HTTP запит з GET параметрами

    Returns:
        HttpResponse: Відрендерена сторінка зі списком оголошень
    """
    ads = Ad.objects.filter(is_active=True).select_related('category', 'user')

    # Фільтрація за категорією
    category_id = request.GET.get('category')
    if category_id:
        ads = ads.filter(category_id=category_id)

    # Фільтрація за ціною
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        ads = ads.filter(price__gte=min_price)
    if max_price:
        ads = ads.filter(price__lte=max_price)

    # Пошук за заголовком
    search_query = request.GET.get('search')
    if search_query:
        ads = ads.filter(title__icontains=search_query)

    # Сортування
    sort_by = request.GET.get('sort', '-created_at')
    allowed_sorts = ['price', '-price', 'created_at', '-created_at']
    if sort_by in allowed_sorts:
        ads = ads.order_by(sort_by)

    categories = Category.objects.all()

    context = {
        'ads': ads,
        'categories': categories,
        'title': 'Всі оголошення'
    }
    return render(request, 'board/ad_list.html', context)


def ad_detail(request: HttpRequest, ad_id: int) -> HttpResponse:
    """
    Детальна сторінка оголошення з коментарями.

    Args:
        request: HTTP запит
        ad_id: ID оголошення

    Returns:
        HttpResponse: Відрендерена сторінка з деталями оголошення
    """
    ad = get_object_or_404(
        Ad.objects.select_related('category', 'user'),
        id=ad_id
    )
    comments = ad.comments.select_related('user')

    context = {
        'ad': ad,
        'comments': comments,
        'comments_count': comments.count(),
        'title': ad.title
    }
    return render(request, 'board/ad_detail.html', context)


def category_list(request: HttpRequest) -> HttpResponse:
    """
    Сторінка зі списком категорій.

    Args:
        request: HTTP запит

    Returns:
        HttpResponse: Відрендерена сторінка зі списком категорій
    """
    categories = Category.objects.annotate(
        active_ads_count=Count('ads', filter=Q(ads__is_active=True))
    )

    context = {
        'categories': categories,
        'title': 'Категорії'
    }
    return render(request, 'board/category_list.html', context)


def category_detail(request: HttpRequest, category_id: int) -> HttpResponse:
    """
    Сторінка категорії з її оголошеннями.

    Args:
        request: HTTP запит
        category_id: ID категорії

    Returns:
        HttpResponse: Відрендерена сторінка категорії
    """
    category = get_object_or_404(Category, id=category_id)
    ads = Ad.objects.filter(
        category=category,
        is_active=True
    ).select_related('user')

    context = {
        'category': category,
        'ads': ads,
        'title': category.name
    }
    return render(request, 'board/category_detail.html', context)


def statistics(request: HttpRequest) -> HttpResponse:
    """
    Сторінка статистики для адміністратора.

    Відображає:
    - Загальну кількість оголошень
    - Кількість активних оголошень
    - Кількість неактивних оголошень
    - Загальну кількість коментарів
    - Статистику по категоріям

    Args:
        request: HTTP запит

    Returns:
        HttpResponse: Відрендерена сторінка статистики
    """
    total_ads = Ad.objects.count()
    active_ads = Ad.objects.filter(is_active=True).count()
    inactive_ads = Ad.objects.filter(is_active=False).count()
    total_comments = Comment.objects.count()

    # Статистика по категоріях
    categories_stats = Category.objects.annotate(
        total_ads=Count('ads'),
        active_ads=Count('ads', filter=Q(ads__is_active=True))
    )

    context = {
        'total_ads': total_ads,
        'active_ads': active_ads,
        'inactive_ads': inactive_ads,
        'total_comments': total_comments,
        'categories_stats': categories_stats,
        'title': 'Статистика'
    }
    return render(request, 'board/statistics.html', context)


@login_required
def ad_create(request: HttpRequest) -> HttpResponse:
    """
    Створення нового оголошення.

    GET: Відображає форму для створення оголошення
    POST: Обробляє дані форми та створює нове оголошення

    Args:
        request: HTTP запит

    Returns:
        HttpResponse: Відрендерена сторінка з формою або редірект
    """
    if request.method == 'POST':
        form = AdCreateForm(request.POST)
        if form.is_valid():
            # Зберегти оголошення з поточним користувачем
            ad = form.save(user=request.user)

            messages.success(
                request,
                f'Оголошення "{ad.title}" успішно створено!'
            )
            return redirect('board:ad_detail', ad_id=ad.id)
        else:
            messages.error(
                request,
                'Помилка при створенні оголошення. Перевірте введені дані.'
            )
    else:
        form = AdCreateForm()

    context = {
        'form': form,
        'title': 'Створити оголошення',
        'button_text': 'Створити'
    }
    return render(request, 'board/ad_form.html', context)


@login_required
def ad_update(request: HttpRequest, ad_id: int) -> HttpResponse:
    """
    Редагування існуючого оголошення.

    GET: Відображає форму з даними оголошення
    POST: Оновлює оголошення

    Args:
        request: HTTP запит
        ad_id: ID оголошення

    Returns:
        HttpResponse: Відрендерена сторінка з формою або редірект
    """
    ad = get_object_or_404(Ad, id=ad_id)

    # Перевірка: тільки автор може редагувати
    if ad.user != request.user:
        messages.error(
            request,
            'Ви не можете редагувати це оголошення.'
        )
        return redirect('board:ad_detail', ad_id=ad.id)

    if request.method == 'POST':
        form = AdUpdateForm(request.POST, instance=ad)
        if form.is_valid():
            ad = form.save()
            messages.success(
                request,
                f'Оголошення "{ad.title}" успішно оновлено!'
            )
            return redirect('board:ad_detail', ad_id=ad.id)
        else:
            messages.error(
                request,
                'Помилка при оновленні оголошення. Перевірте введені дані.'
            )
    else:
        form = AdUpdateForm(instance=ad)

    context = {
        'form': form,
        'ad': ad,
        'title': f'Редагувати: {ad.title}',
        'button_text': 'Зберегти зміни'
    }
    return render(request, 'board/ad_form.html', context)


@login_required
def ad_delete(request: HttpRequest, ad_id: int) -> HttpResponse:
    """
    Видалення оголошення.

    GET: Відображає сторінку підтвердження
    POST: Видаляє оголошення

    Args:
        request: HTTP запит
        ad_id: ID оголошення

    Returns:
        HttpResponse: Відрендерена сторінка або редірект
    """
    ad = get_object_or_404(Ad, id=ad_id)

    # Перевірка: тільки автор може видаляти
    if ad.user != request.user:
        messages.error(
            request,
            'Ви не можете видалити це оголошення.'
        )
        return redirect('board:ad_detail', ad_id=ad.id)

    if request.method == 'POST':
        ad_title = ad.title
        ad.delete()
        messages.success(
            request,
            f'Оголошення "{ad_title}" успішно видалено!'
        )
        return redirect('board:index')

    context = {
        'ad': ad,
        'title': f'Видалити: {ad.title}'
    }
    return render(request, 'board/ad_confirm_delete.html', context)


@login_required
def comment_create(request: HttpRequest, ad_id: int) -> HttpResponse:
    """
    Додавання коментаря до оголошення.

    POST: Створює новий коментар

    Args:
        request: HTTP запит
        ad_id: ID оголошення

    Returns:
        HttpResponse: Редірект на сторінку оголошення
    """
    ad = get_object_or_404(Ad, id=ad_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ad = ad
            comment.user = request.user
            comment.save()

            messages.success(
                request,
                'Коментар успішно додано!'
            )
        else:
            messages.error(
                request,
                'Помилка при додаванні коментаря. Перевірте введені дані.'
            )

    return redirect('board:ad_detail', ad_id=ad_id)


@login_required
def my_ads(request: HttpRequest) -> HttpResponse:
    """
    Сторінка з оголошеннями поточного користувача.

    Args:
        request: HTTP запит

    Returns:
        HttpResponse: Відрендерена сторінка
    """
    ads = Ad.objects.filter(
        user=request.user
    ).select_related('category').order_by('-created_at')

    context = {
        'ads': ads,
        'title': 'Мої оголошення'
    }
    return render(request, 'board/my_ads.html', context)
