# blog/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Article, Comment, Tag, Category, CustomUser


# ========== ЗАВДАННЯ 3: Кастомна адмінка з фільтрами та діями ==========

# Inline-моделі для пов'язаного відображення
class CommentInline(admin.TabularInline):
    """Inline відображення коментарів"""
    model = Comment
    extra = 0
    fields = ['author', 'content', 'is_approved', 'created_at']
    readonly_fields = ['created_at']
    can_delete = True


class TagInline(admin.TabularInline):
    """Inline відображення тегів"""
    model = Tag.articles.through
    extra = 1


# Кастомні фільтри
class ViewsCountFilter(admin.SimpleListFilter):
    """Фільтр за кількістю переглядів"""
    title = 'Популярність'
    parameter_name = 'views'

    def lookups(self, request, model_admin):
        return [
            ('low', 'Менше 100 переглядів'),
            ('medium', '100-1000 переглядів'),
            ('high', 'Більше 1000 переглядів'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(views_count__lt=100)
        if self.value() == 'medium':
            return queryset.filter(views_count__gte=100, views_count__lte=1000)
        if self.value() == 'high':
            return queryset.filter(views_count__gt=1000)


class RecentArticlesFilter(admin.SimpleListFilter):
    """Фільтр за датою створення"""
    title = 'Дата створення'
    parameter_name = 'recent'

    def lookups(self, request, model_admin):
        return [
            ('today', 'Сьогодні'),
            ('week', 'Цього тижня'),
            ('month', 'Цього місяця'),
        ]

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == 'today':
            return queryset.filter(created_at__date=now.date())
        if self.value() == 'week':
            week_ago = now - timedelta(days=7)
            return queryset.filter(created_at__gte=week_ago)
        if self.value() == 'month':
            month_ago = now - timedelta(days=30)
            return queryset.filter(created_at__gte=month_ago)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Адміністрування статей"""

    list_display = [
        'title', 'author', 'status', 'views_count',
        'comment_count', 'created_at', 'colored_status'
    ]
    list_filter = [
        'status', ViewsCountFilter, RecentArticlesFilter,
        'created_at', 'updated_at'
    ]
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ['views_count', 'created_at', 'updated_at', 'statistics_display']

    fieldsets = (
        ('Основна інформація', {
            'fields': ('title', 'slug', 'author', 'status')
        }),
        ('Контент', {
            'fields': ('content', 'metadata'),
            'classes': ('wide',)
        }),
        ('Статистика', {
            'fields': ('views_count', 'statistics_display', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    inlines = [CommentInline, TagInline]

    # Кастомні дії
    actions = ['publish_articles', 'archive_articles', 'reset_views']

    def get_queryset(self, request):
        """Оптимізований queryset з підрахунком коментарів"""
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _comment_count=Count('comments', distinct=True)
        )
        return queryset

    @admin.display(description='Коментарі', ordering='_comment_count')
    def comment_count(self, obj):
        """Відображення кількості коментарів"""
        count = obj._comment_count
        return format_html(
            '<span style="background: #4CAF50; color: white; '
            'padding: 3px 8px; border-radius: 3px;">{}</span>',
            count
        )

    @admin.display(description='Статус')
    def colored_status(self, obj):
        """Кольоровий статус"""
        colors = {
            'draft': '#FFA500',
            'published': '#4CAF50',
            'archived': '#9E9E9E',
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">●</span> {}',
            colors.get(obj.status, '#000'),
            obj.get_status_display()
        )

    @admin.display(description='Статистика')
    def statistics_display(self, obj):
        """Відображення статистики статті"""
        stats = obj.get_statistics()
        return format_html(
            '<strong>Слів:</strong> {} | '
            '<strong>Символів:</strong> {} | '
            '<strong>Час читання:</strong> {} хв',
            stats['words'],
            stats['characters'],
            stats['reading_time']
        )

    # Кастомні дії для статей
    @admin.action(description='Опублікувати вибрані статті')
    def publish_articles(self, request, queryset):
        """Масова публікація статей"""
        updated = queryset.update(status='published')
        self.message_user(
            request,
            f'Успішно опубліковано {updated} статей.'
        )

    @admin.action(description='Архівувати вибрані статті')
    def archive_articles(self, request, queryset):
        """Масове архівування статей"""
        updated = queryset.update(status='archived')
        self.message_user(
            request,
            f'Успішно архівовано {updated} статей.'
        )

    @admin.action(description='Скинути лічильник переглядів')
    def reset_views(self, request, queryset):
        """Скидання лічильника переглядів"""
        updated = queryset.update(views_count=0)
        self.message_user(
            request,
            f'Лічильник переглядів скинуто для {updated} статей.'
        )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Адміністрування коментарів"""

    list_display = [
        'author', 'article', 'short_content',
        'is_approved', 'created_at'
    ]
    list_filter = ['is_approved', 'created_at']
    search_fields = ['content', 'author__username', 'article__title']
    date_hierarchy = 'created_at'
    actions = ['approve_comments', 'reject_comments']

    fieldsets = (
        (None, {
            'fields': ('article', 'author', 'parent')
        }),
        ('Контент', {
            'fields': ('content', 'is_approved')
        }),
        ('Метадані', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at']

    @admin.display(description='Коментар')
    def short_content(self, obj):
        """Скорочений текст коментаря"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    @admin.action(description='Схвалити вибрані коментарі')
    def approve_comments(self, request, queryset):
        """Масове схвалення коментарів"""
        updated = queryset.update(is_approved=True)
        self.message_user(
            request,
            f'Успішно схвалено {updated} коментарів.'
        )

    @admin.action(description='Відхилити вибрані коментарі')
    def reject_comments(self, request, queryset):
        """Масове відхилення коментарів"""
        updated = queryset.update(is_approved=False)
        self.message_user(
            request,
            f'Успішно відхилено {updated} коментарів.'
        )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Адміністрування тегів"""

    list_display = ['name', 'article_count_display', 'colored_popularity']
    search_fields = ['name']
    ordering = ['name']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _article_count=Count('articles', filter=Q(articles__status='published'))
        )
        return queryset

    @admin.display(description='Статті', ordering='_article_count')
    def article_count_display(self, obj):
        """Відображення кількості статей"""
        count = obj._article_count
        return format_html(
            '<strong>{}</strong> статей',
            count
        )

    @admin.display(description='Популярність')
    def colored_popularity(self, obj):
        """Кольоровий індикатор популярності"""
        count = obj._article_count
        if count > 10:
            color = '#4CAF50'
            text = 'Високa'
        elif count > 5:
            color = '#FFA500'
            text = 'Середня'
        else:
            color = '#9E9E9E'
            text = 'Низька'

        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            text
        )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Адміністрування категорій"""

    list_display = ['name', 'parent', 'slug']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['parent']


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Адміністрування користувачів"""

    list_display = [
        'username', 'email', 'phone_number',
        'is_staff', 'date_joined', 'article_count'
    ]
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'phone_number']

    fieldsets = UserAdmin.fieldsets + (
        ('Додаткова інформація', {
            'fields': ('phone_number', 'bio', 'birth_date', 'avatar')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Додаткова інформація', {
            'fields': ('email', 'phone_number', 'bio', 'birth_date')
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _article_count=Count('articles')
        )
        return queryset

    @admin.display(description='Статті', ordering='_article_count')
    def article_count(self, obj):
        """Відображення кількості статей автора"""
        count = obj._article_count
        return format_html(
            '<span style="background: #2196F3; color: white; '
            'padding: 3px 8px; border-radius: 3px;">{}</span>',
            count
        )


# Налаштування адмін-панелі
admin.site.site_header = "Адміністрування блогу"
admin.site.site_title = "Блог Admin"
admin.site.index_title = "Панель управління"