# Команда для відображення метрик

from django.core.management.base import BaseCommand
from blog.metrics import BlogMetrics, request_metrics
import json


class Command(BaseCommand):
    help = 'Показати метрики блогу'

    def handle(self, *args, **options):
        metrics = BlogMetrics.get_all_metrics()

        self.stdout.write(self.style.SUCCESS('=== Метрики блогу ===\n'))

        # Статті
        self.stdout.write(self.style.SUCCESS('Статті:'))
        for key, value in metrics['articles'].items():
            if key != 'most_viewed':
                self.stdout.write(f"  {key}: {value}")

        # Коментарі
        self.stdout.write(self.style.SUCCESS('\nКоментарі:'))
        for key, value in metrics['comments'].items():
            self.stdout.write(f"  {key}: {value}")

        # Користувачі
        self.stdout.write(self.style.SUCCESS('\nКористувачі:'))
        for key, value in metrics['users'].items():
            self.stdout.write(f"  {key}: {value}")

        # Топ запитів
        self.stdout.write(self.style.SUCCESS('\nТоп-10 запитів:'))
        for stat in metrics['requests'][:10]:
            self.stdout.write(
                f"  {stat['path']}: "
                f"{stat['requests']} запитів, "
                f"середній час: {stat['avg_time']:.3f}s"
            )