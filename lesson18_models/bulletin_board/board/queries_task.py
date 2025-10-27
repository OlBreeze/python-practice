"""
Приклади ORM запитів для дошки оголошень.

Цей модуль містить функції з різними запитами до бази даних
для демонстрації можливостей Django ORM.
"""
# Додаємо шлях до проєкту
import os
import sys
import django


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Налаштування Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulletin_board.settings')
django.setup()

from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Q, Avg, Max, Min, QuerySet
from board.models import Ad, Category, Comment
from django.contrib.auth.models import User


def get_ads_last_month() -> QuerySet[Ad]:
    """
    Отримує всі оголошення, створені за останній місяць.

    Returns:
        QuerySet[Ad]: Набір оголошень за останній місяць
    """
    one_month_ago = timezone.now() - timedelta(days=30)
    return Ad.objects.filter(created_at__gte=one_month_ago)


def get_active_ads_by_category(category_id: int) -> QuerySet[Ad]:
    """
    Отримує всі активні оголошення в певній категорії.

    Args:
        category_id: ID категорії

    Returns:
        QuerySet[Ad]: Набір активних оголошень у категорії
    """
    return Ad.objects.filter(
        category_id=category_id,
        is_active=True
    ).select_related('user', 'category')


def get_ads_with_comments_count() -> QuerySet[Ad]:
    """
    Отримує всі оголошення з кількістю коментарів до кожного.

    Returns:
        QuerySet[Ad]: Набір оголошень з анотованою кількістю коментарів
    """
    return Ad.objects.annotate(
        comments_count=Count('comments')
    ).select_related('user', 'category')


def get_user_ads(user_id: int) -> QuerySet[Ad]:
    """
    Отримує всі оголошення певного користувача.

    Args:
        user_id: ID користувача

    Returns:
        QuerySet[Ad]: Набір оголошень користувача
    """
    return Ad.objects.filter(user_id=user_id).select_related('category')


def get_categories_with_ads_count() -> QuerySet[Category]:
    """
    Отримує всі категорії з кількістю оголошень.

    Returns:
        QuerySet[Category]: Набір категорій з кількістю оголошень
    """
    return Category.objects.annotate(
        total_ads=Count('ads'),
        active_ads=Count('ads', filter=Q(ads__is_active=True))
    )


def get_most_commented_ads(limit: int = 10) -> QuerySet[Ad]:
    """
    Отримує найбільш коментовані оголошення.

    Args:
        limit: Максимальна кількість оголошень для повернення

    Returns:
        QuerySet[Ad]: Набір найбільш коментованих оголошень
    """
    return Ad.objects.annotate(
        comments_count=Count('comments')
    ).order_by('-comments_count')[:limit]


def get_expensive_ads(min_price: float = 1000) -> QuerySet[Ad]:
    """
    Отримує оголошення з ціною вище вказаної.

    Args:
        min_price: Мінімальна ціна

    Returns:
        QuerySet[Ad]: Набір дорогих оголошень
    """
    return Ad.objects.filter(
        price__gte=min_price,
        is_active=True
    ).select_related('user', 'category')


def get_users_with_multiple_ads(min_ads: int = 3) -> QuerySet[User]:
    """
    Отримує користувачів, які створили більше вказаної кількості оголошень.

    Args:
        min_ads: Мінімальна кількість оголошень

    Returns:
        QuerySet[User]: Набір користувачів з багатьма оголошеннями
    """
    return User.objects.annotate(
        ads_count=Count('ads')
    ).filter(ads_count__gte=min_ads)


def get_category_statistics(category_id: int) -> dict:
    """
    Отримує статистику по категорії.

    Args:
        category_id: ID категорії

    Returns:
        dict: Словник зі статистикою категорії
    """
    stats = Ad.objects.filter(category_id=category_id).aggregate(
        total_ads=Count('id'),
        active_ads=Count('id', filter=Q(is_active=True)),
        avg_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price'),
        total_comments=Count('comments')
    )
    return stats


def search_ads(query: str) -> QuerySet[Ad]:
    """
    Пошук оголошень за заголовком або описом.

    Args:
        query: Пошуковий запит

    Returns:
        QuerySet[Ad]: Набір знайдених оголошень
    """
    return Ad.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query),
        is_active=True
    ).select_related('user', 'category')


def get_expired_ads() -> QuerySet[Ad]:
    """
    Отримує оголошення, які мають бути деактивовані (старше 30 днів).

    Returns:
        QuerySet[Ad]: Набір застарілих оголошень
    """
    thirty_days_ago = timezone.now() - timedelta(days=30)
    return Ad.objects.filter(
        created_at__lt=thirty_days_ago,
        is_active=True
    )


def get_recent_comments(limit: int = 10) -> QuerySet[Comment]:
    """
    Отримує найновіші коментарі.

    Args:
        limit: Максимальна кількість коментарів

    Returns:
        QuerySet[Comment]: Набір останніх коментарів
    """
    return Comment.objects.select_related(
        'user', 'ad'
    ).order_by('-created_at')[:limit]


def get_ads_by_price_range(min_price: float, max_price: float) -> QuerySet[Ad]:
    """
    Отримує оголошення в заданому діапазоні цін.

    Args:
        min_price: Мінімальна ціна
        max_price: Максимальна ціна

    Returns:
        QuerySet[Ad]: Набір оголошень у діапазоні цін
    """
    return Ad.objects.filter(
        price__gte=min_price,
        price__lte=max_price,
        is_active=True
    ).select_related('user', 'category')


# Приклад використання функцій:
if __name__ == '__main__':
    # Отримати оголошення за останній місяць
    recent_ads = get_ads_last_month()
    print(f"Оголошень за місяць: {recent_ads.count()}")

    # Отримати активні оголошення в категорії з ID=1
    category_ads = get_active_ads_by_category(1)
    print(f"Активних оголошень у категорії: {category_ads.count()}")

    # Отримати оголошення з кількістю коментарів
    ads_with_comments = get_ads_with_comments_count()
    for ad in ads_with_comments:
        print(f"{ad.title}: {ad.comments_count} коментарів")

    # Отримати всі оголошення користувача
    user_ads = get_user_ads(1)
    print(f"Оголошень користувача: {user_ads.count()}")
