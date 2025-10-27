"""
Моделі для застосунку дошки оголошень.

Цей модуль містить моделі для роботи з оголошеннями, категоріями,
коментарями та профілями користувачів.
"""

from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class UserProfile(models.Model):
    """
    Розширення моделі користувача додатковими полями.

    Attributes:
        user (User): Зв'язок один-до-одного з вбудованою моделлю User
        phone_number (str): Номер телефону користувача
        address (str): Адреса користувача
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Користувач'
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Номер телефону'
    )
    address = models.TextField(
        blank=True,
        verbose_name='Адреса'
    )

    class Meta:
        verbose_name = 'Профіль користувача'
        verbose_name_plural = 'Профілі користувачів'

    def __str__(self) -> str:
        """Повертає рядкове представлення профілю."""
        return f"Профіль {self.user.username}"


class Category(models.Model):
    """
    Модель категорії оголошень.

    Attributes:
        name (str): Унікальна назва категорії
        description (str): Опис категорії
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Назва категорії'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Опис категорії'
    )

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['name']

    def __str__(self) -> str:
        """Повертає рядкове представлення категорії."""
        return self.name

    def get_active_ads_count(self) -> int:
        """
        Підраховує кількість активних оголошень у категорії.

        Returns:
            int: Кількість активних оголошень
        """
        return self.ads.filter(is_active=True).count()


class Ad(models.Model):
    """
    Модель оголошення.

    Attributes:
        title (str): Заголовок оголошення
        description (str): Повний опис оголошення
        price (Decimal): Ціна товару/послуги
        created_at (datetime): Дата та час створення
        updated_at (datetime): Дата та час останнього оновлення
        is_active (bool): Статус активності оголошення
        user (User): Користувач, який створив оголошення
        category (Category): Категорія оголошення
    """
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        verbose_name='Опис'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Ціна'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата створення'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата оновлення'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активне'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ads',
        verbose_name='Користувач'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='ads',
        verbose_name='Категорія'
    )

    class Meta:
        verbose_name = 'Оголошення'
        verbose_name_plural = 'Оголошення'
        ordering = ['-created_at']

    def __str__(self) -> str:
        """Повертає рядкове представлення оголошення."""
        return self.title

    def get_short_description(self) -> str:
        """
        Повертає скорочений опис оголошення (до 100 символів).

        Returns:
            str: Скорочений опис з трьома крапками, якщо він довший за 100 символів
        """
        if len(self.description) > 100:
            return f"{self.description[:100]}..."
        return self.description

    def deactivate_if_expired(self) -> bool:
        """
        Деактивує оголошення, якщо минуло 30 днів з моменту створення.

        Returns:
            bool: True, якщо оголошення було деактивовано, False - якщо ні
        """
        if self.is_active:
            expiration_date = self.created_at + timedelta(days=30)
            if timezone.now() >= expiration_date:
                self.is_active = False
                self.save()
                return True
        return False

    def clean(self) -> None:
        """
        Валідація моделі перед збереженням.

        Raises:
            ValidationError: Якщо ціна не є додатним числом
        """
        super().clean()
        if self.price is not None and self.price <= 0:
            raise ValidationError({
                'price': 'Ціна повинна бути додатним числом.'
            })


class Comment(models.Model):
    """
    Модель коментаря до оголошення.

    Attributes:
        content (str): Текст коментаря
        created_at (datetime): Дата та час створення коментаря
        ad (Ad): Оголошення, до якого відноситься коментар
        user (User): Користувач, який залишив коментар
    """
    content = models.TextField(
        verbose_name='Текст коментаря'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата створення'
    )
    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Оголошення'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Користувач'
    )

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'
        ordering = ['-created_at']

    def __str__(self) -> str:
        """Повертає рядкове представлення коментаря."""
        return f"Коментар від {self.user.username} до {self.ad.title}"

    @staticmethod
    def get_comments_count_for_ad(ad: 'Ad') -> int:
        """
        Підраховує кількість коментарів до оголошення.

        Args:
            ad (Ad): Оголошення, для якого підраховуються коментарі

        Returns:
            int: Кількість коментарів
        """
        return ad.comments.count()