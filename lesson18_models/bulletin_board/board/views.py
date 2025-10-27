"""
Представлення (views) для застосунку дошки оголошень.

Цей модуль містить функції для відображення списків оголошень,
деталей оголошень, категорій та статистики.
"""

from typing import Any
from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.db.models import Count, Q, QuerySet
from .models import Ad, Category, Comment


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
