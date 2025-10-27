"""
Management команда для деактивації застарілих оголошень.

Використання:
    python manage.py deactivate_expired_ads
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from lesson18_models.bulletin_board.board.models import Ad


# from board.models import Ad


class Command(BaseCommand):
    """
    Команда для деактивації оголошень, яким виповнилося 30 днів.
    """

    help = 'Деактивує оголошення, які були створені більше 30 днів тому'

    def handle(self, *args, **options) -> None:
        """
        Виконує деактивацію застарілих оголошень.

        Args:
            *args: Позиційні аргументи
            **options: Іменовані аргументи
        """
        thirty_days_ago = timezone.now() - timedelta(days=30)

        # Знаходимо всі активні оголошення старше 30 днів
        expired_ads = Ad.objects.filter(
            created_at__lt=thirty_days_ago,
            is_active=True
        )

        count = expired_ads.count()

        if count > 0:
            # Деактивуємо оголошення
            expired_ads.update(is_active=False)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Успішно деактивовано {count} оголошень'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    'Немає оголошень для деактивації'
                )
            )