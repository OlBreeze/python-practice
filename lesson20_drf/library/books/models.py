from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

class Book(models.Model):
    """
        Модель для представлення книги в бібліотеці.

        Attributes:
            title (str): Назва книги (максимум 255 символів)
            author (str): Автор книги (максимум 255 символів)
            genre (str): Жанр книги (максимум 100 символів)
            publication_year (int): Рік видання (тільки позитивні числа)
            user (ForeignKey): Користувач, який створив запис про книгу
            created_at (datetime): Дата і час створення запису
        """

    title = models.CharField(
        max_length=255,
        verbose_name="Назва книги",
        help_text="Введіть назву книги"
    )
    author = models.CharField(
        max_length=255,
        verbose_name="Автор",
        help_text="Введіть ім'я автора книги"
    )
    genre = models.CharField(
        max_length=100,
        verbose_name="Жанр",
        help_text="Введіть жанр книги (наприклад, фантастика, детектив)"
    )
    publication_year = models.PositiveIntegerField(
        verbose_name="Рік видання",
        help_text="Введіть рік видання книги"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name="Користувач",
        help_text="Користувач, який створив запис"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата створення"
    )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['genre']),
            models.Index(fields=['publication_year']),
        ]

    def __str__(self) -> str:
        """Повертає рядкове представлення книги."""
        return f"{self.title} ({self.author}, {self.publication_year})"
