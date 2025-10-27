"""
Адміністративна панель для застосунку дошки оголошень.

Цей модуль налаштовує інтерфейс адміністратора для керування
категоріями, оголошеннями, коментарями та профілями користувачів.
"""

from django.contrib import admin
from django.db.models import Count
from .models import Category, Ad, Comment, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Адміністративний інтерфейс для профілів користувачів.

    Attributes:
        list_display: Поля для відображення в списку
        search_fields: Поля для пошуку
    """
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__username', 'phone_number')
    list_per_page = 20


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Адміністративний інтерфейс для категорій.

    Attributes:
        list_display: Поля для відображення в списку
        search_fields: Поля для пошуку
    """
    list_display = ('name', 'description', 'active_ads_count')
    search_fields = ('name', 'description')
    list_per_page = 20

    def active_ads_count(self, obj: Category) -> int:
        """
        Відображає кількість активних оголошень в категорії.

        Args:
            obj: Екземпляр категорії

        Returns:
            int: Кількість активних оголошень
        """
        return obj.get_active_ads_count()

    active_ads_count.short_description = 'Активних оголошень'


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """
    Адміністративний інтерфейс для оголошень.

    Attributes:
        list_display: Поля для відображення в списку
        list_filter: Поля для фільтрації
        search_fields: Поля для пошуку
        readonly_fields: Поля тільки для читання
        fieldsets: Організація полів у формі
    """
    list_display = (
        'title',
        'category',
        'user',
        'price',
        'is_active',
        'created_at',
        'comments_count'
    )
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20

    fieldsets = (
        ('Основна інформація', {
            'fields': ('title', 'description', 'price', 'category')
        }),
        ('Користувач', {
            'fields': ('user',)
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
        ('Дати', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """
        Оптимізує запит додаванням підрахунку коментарів.

        Args:
            request: HTTP запит

        Returns:
            QuerySet: Оптимізований набір оголошень
        """
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _comments_count=Count('comments')
        )
        return queryset

    def comments_count(self, obj: Ad) -> int:
        """
        Відображає кількість коментарів до оголошення.

        Args:
            obj: Екземпляр оголошення

        Returns:
            int: Кількість коментарів
        """
        return obj._comments_count

    comments_count.short_description = 'Коментарів'
    comments_count.admin_order_field = '_comments_count'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Адміністративний інтерфейс для коментарів.

    Attributes:
        list_display: Поля для відображення в списку
        list_filter: Поля для фільтрації
        search_fields: Поля для пошуку
        readonly_fields: Поля тільки для читання
    """
    list_display = ('user', 'ad', 'short_content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username', 'ad__title')
    readonly_fields = ('created_at',)
    list_per_page = 20

    def short_content(self, obj: Comment) -> str:
        """
        Відображає скорочений текст коментаря.

        Args:
            obj: Екземпляр коментаря

        Returns:
            str: Скорочений текст коментаря
        """
        if len(obj.content) > 50:
            return f"{obj.content[:50]}..."
        return obj.content

    short_content.short_description = 'Коментар'