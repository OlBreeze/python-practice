from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Адмін-панель для управління книгами."""

    # Відображення полів у списку
    list_display = [
        'id',
        'title',
        'author',
        'genre',
        'publication_year',
        'user',
        'created_at'
    ]

    # Поля, які можна редагувати прямо в списку
    list_editable = ['title', 'author', 'genre', 'publication_year']

    # Пошук
    search_fields = ['title', 'author', 'genre']

    # Фільтри
    list_filter = [
        'genre',
        'publication_year',
        'user',
        'created_at'
    ]

    # Сортування за замовчуванням
    ordering = ['-created_at']

    # Кількість елементів на сторінці
    list_per_page = 20

    # Поля тільки для читання
    readonly_fields = ['created_at', 'id']

    # Організація полів у формі редагування
    fieldsets = (
        ('Основна інформація', {
            'fields': ('title', 'author', 'genre', 'publication_year')
        }),
        ('Метадані', {
            'fields': ('user', 'created_at', 'id'),
            'classes': ('collapse',)
        }),
    )

    # Автозаповнення для ForeignKey
    autocomplete_fields = ['user']

    # Експорт в CSV
    actions = ['export_to_csv']

    def export_to_csv(self, request, queryset):
        """Експорт вибраних книг у CSV."""
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="books.csv"'

        # Додаємо BOM для правильного відображення кирилиці в Excel
        response.write('\ufeff')

        writer = csv.writer(response)
        writer.writerow(['ID', 'Назва', 'Автор', 'Жанр', 'Рік', 'Користувач', 'Дата створення'])

        for book in queryset:
            writer.writerow([
                book.id,
                book.title,
                book.author,
                book.genre,
                book.publication_year,
                book.user.username,
                book.created_at.strftime('%Y-%m-%d %H:%M')
            ])

        self.message_user(request, f'Експортовано {queryset.count()} книг')
        return response

    export_to_csv.short_description = 'Експортувати вибрані книги в CSV'

    def get_queryset(self, request):
        """Оптимізація запитів до БД."""
        qs = super().get_queryset(request)
        return qs.select_related('user')


# Inline для відображення книг користувача
class BookInline(admin.TabularInline):
    """Показ книг в профілі користувача."""
    model = Book
    extra = 0
    fields = ['title', 'author', 'genre', 'publication_year', 'created_at']
    readonly_fields = ['created_at']
    can_delete = True


class CustomUserAdmin(BaseUserAdmin):
    """Розширена адмінка для користувачів."""
    inlines = [BookInline]

    list_display = BaseUserAdmin.list_display + ('books_count',)

    def books_count(self, obj):
        """Кількість книг користувача."""
        count = obj.books.count()
        return format_html(
            '<span style="background: #4caf50; color: white; padding: 2px 8px; '
            'border-radius: 10px; font-weight: bold;">{}</span>',
            count
        )

    books_count.short_description = '📚 Книг'


# Перереєстрація User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Налаштування заголовків
admin.site.site_header = "📚 Адміністрування бібліотеки"
admin.site.site_title = "Бібліотека - Адмін"
admin.site.index_title = "Панель управління"