# blog/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import json
import re


# ========== ЗАВДАННЯ 10: Кастомні поля моделі ==========
class UpperCaseCharField(models.CharField):
    """Поле, яке автоматично конвертує текст у верхній регістр"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value:
            return value.upper()
        return value


class PhoneNumberField(models.CharField):
    """Кастомне поле для телефонних номерів"""

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 13
        kwargs['validators'] = [
            RegexValidator(
                regex=r'^\+380\d{9}$',
                message='Телефон повинен бути у форматі +380XXXXXXXXX'
            )
        ]
        super().__init__(*args, **kwargs)


class JSONField(models.TextField):
    """Поле для зберігання JSON даних (для старих версій Django)"""

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return json.loads(value)

    def to_python(self, value):
        if isinstance(value, dict) or isinstance(value, list):
            return value
        if value is None:
            return value
        return json.loads(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return json.dumps(value, ensure_ascii=False)


# ========== ЗАВДАННЯ 1 та 6: Кастомна модель користувача ==========
class CustomUser(AbstractUser):
    """Розширена модель користувача з додатковими полями"""

    phone_number = PhoneNumberField(
        verbose_name="Номер телефону",
        blank=True,
        null=True
    )
    bio = models.TextField(
        verbose_name="Біографія",
        max_length=500,
        blank=True
    )
    birth_date = models.DateField(
        verbose_name="Дата народження",
        null=True,
        blank=True
    )
    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to='avatars/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

    def __str__(self):
        return self.username


# ========== ЗАВДАННЯ 1: Модель з обробкою даних ==========
class Article(models.Model):
    """Модель статті блогу"""

    STATUS_CHOICES = [
        ('draft', 'Чернетка'),
        ('published', 'Опубліковано'),
        ('archived', 'Архів'),
    ]

    title = UpperCaseCharField(
        verbose_name="Заголовок",
        max_length=200
    )
    slug = models.SlugField(
        verbose_name="URL",
        max_length=200,
        unique=True
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name="Автор"
    )
    content = models.TextField(verbose_name="Контент")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Статус"
    )
    metadata = JSONField(
        verbose_name="Метадані",
        blank=True,
        null=True,
        help_text="JSON дані (теги, категорії тощо)"
    )
    views_count = models.IntegerField(
        default=0,
        verbose_name="Кількість переглядів"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата створення"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата оновлення"
    )

    class Meta:
        verbose_name = "Стаття"
        verbose_name_plural = "Статті"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.title

    # Методи обробки даних
    def get_reading_time(self):
        """Підрахунок часу читання (середня швидкість 200 слів/хв)"""
        word_count = len(self.content.split())
        minutes = word_count / 200
        return max(1, round(minutes))

    def get_statistics(self):
        """Підрахунок статистики статті"""
        return {
            'words': len(self.content.split()),
            'characters': len(self.content),
            'comments': self.comments.count(),
            'views': self.views_count,
            'reading_time': self.get_reading_time(),
        }

    def increment_views(self):
        """Збільшення лічильника переглядів"""
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def is_published(self):
        """Перевірка чи опублікована стаття"""
        return self.status == 'published'


class Comment(models.Model):
    """Модель коментаря до статті"""

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Стаття"
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Автор"
    )
    content = models.TextField(verbose_name="Текст коментаря")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name="Відповідь на"
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name="Схвалено"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата створення"
    )

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}"


class Tag(models.Model):
    """Модель тегу"""

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Назва"
    )
    articles = models.ManyToManyField(
        Article,
        related_name='tags',
        verbose_name="Статті"
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name

    def get_article_count(self):
        """Кількість статей з цим тегом"""
        return self.articles.filter(status='published').count()


class Category(models.Model):
    """Модель категорії"""

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Назва"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="URL"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Опис"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Батьківська категорія"
    )

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name