import time
from functools import wraps
from collections import defaultdict
from threading import Lock
from datetime import datetime, timedelta
from django.core.cache import cache
from django.db.models import Count, Avg
from .models import Article, Comment, CustomUser


class RequestMetrics:
    """Клас для збору метрик запитів"""

    def __init__(self):
        self.metrics = defaultdict(lambda: {
            'count': 0,
            'total_time': 0,
            'errors': 0,
            'last_access': None,
        })
        self.lock = Lock()

    def record_request(self, path, duration, success=True):
        """Записати метрику запиту"""
        with self.lock:
            metric = self.metrics[path]
            metric['count'] += 1
            metric['total_time'] += duration
            metric['last_access'] = datetime.now()
            if not success:
                metric['errors'] += 1

    def get_stats(self, path=None):
        """Отримати статистику"""
        if path:
            metric = self.metrics.get(path, {})
            if metric.get('count', 0) > 0:
                return {
                    'path': path,
                    'requests': metric['count'],
                    'avg_time': metric['total_time'] / metric['count'],
                    'errors': metric['errors'],
                    'error_rate': metric['errors'] / metric['count'] * 100,
                    'last_access': metric['last_access'],
                }
            return {}

        # Всі метрики
        stats = []
        for path, metric in self.metrics.items():
            if metric['count'] > 0:
                stats.append({
                    'path': path,
                    'requests': metric['count'],
                    'avg_time': metric['total_time'] / metric['count'],
                    'errors': metric['errors'],
                    'error_rate': metric['errors'] / metric['count'] * 100,
                    'last_access': metric['last_access'],
                })

        return sorted(stats, key=lambda x: x['requests'], reverse=True)

    def reset(self):
        """Скинути метрики"""
        with self.lock:
            self.metrics.clear()


# Глобальний екземпляр
request_metrics = RequestMetrics()


class MetricsMiddleware:
    """Middleware для збору метрик запитів"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        # Обробка запиту
        response = self.get_response(request)

        # Розрахунок часу
        duration = time.time() - start_time

        # Запис метрики
        success = 200 <= response.status_code < 400
        request_metrics.record_request(
            request.path,
            duration,
            success
        )

        # Додаємо метрику до заголовків
        response['X-Response-Time'] = f'{duration:.3f}s'

        return response


def track_execution_time(func):
    """Декоратор для відстеження часу виконання функції"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time

        import logging
        logger = logging.getLogger('blog')
        logger.info(
            f"Function '{func.__name__}' executed in {duration:.3f}s"
        )

        return result

    return wrapper


class BlogMetrics:
    """Клас для збору метрик блогу"""

    CACHE_TIMEOUT = 300  # 5 хвилин

    @staticmethod
    def get_article_metrics():
        """Метрики статей"""
        cache_key = 'metrics:articles'
        cached = cache.get(cache_key)

        if cached:
            return cached

        metrics = {
            'total': Article.objects.count(),
            'published': Article.objects.filter(status='published').count(),
            'draft': Article.objects.filter(status='draft').count(),
            'archived': Article.objects.filter(status='archived').count(),
            'total_views': Article.objects.aggregate(
                total=Count('views_count')
            )['total'] or 0,
            'avg_views': Article.objects.filter(
                status='published'
            ).aggregate(avg=Avg('views_count'))['avg'] or 0,
            'most_viewed': Article.objects.filter(
                status='published'
            ).order_by('-views_count').first(),
        }

        cache.set(cache_key, metrics, BlogMetrics.CACHE_TIMEOUT)
        return metrics

    @staticmethod
    def get_comment_metrics():
        """Метрики коментарів"""
        cache_key = 'metrics:comments'
        cached = cache.get(cache_key)

        if cached:
            return cached

        metrics = {
            'total': Comment.objects.count(),
            'approved': Comment.objects.filter(is_approved=True).count(),
            'pending': Comment.objects.filter(is_approved=False).count(),
            'avg_per_article': Comment.objects.values('article').annotate(
                count=Count('id')
            ).aggregate(avg=Avg('count'))['avg'] or 0,
        }

        cache.set(cache_key, metrics, BlogMetrics.CACHE_TIMEOUT)
        return metrics

    @staticmethod
    def get_user_metrics():
        """Метрики користувачів"""
        cache_key = 'metrics:users'
        cached = cache.get(cache_key)

        if cached:
            return cached

        metrics = {
            'total': CustomUser.objects.count(),
            'active_authors': CustomUser.objects.filter(
                articles__status='published'
            ).distinct().count(),
            'avg_articles_per_author': CustomUser.objects.annotate(
                article_count=Count('articles')
            ).aggregate(avg=Avg('article_count'))['avg'] or 0,
        }

        cache.set(cache_key, metrics, BlogMetrics.CACHE_TIMEOUT)
        return metrics

    @staticmethod
    def get_daily_stats(days=7):
        """Денна статистика за останні N днів"""
        from django.utils import timezone

        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)

        articles_by_day = Article.objects.filter(
            created_at__gte=start_date
        ).extra(
            select={'day': 'date(created_at)'}
        ).values('day').annotate(count=Count('id')).order_by('day')

        comments_by_day = Comment.objects.filter(
            created_at__gte=start_date
        ).extra(
            select={'day': 'date(created_at)'}
        ).values('day').annotate(count=Count('id')).order_by('day')

        return {
            'articles': list(articles_by_day),
            'comments': list(comments_by_day),
        }

    @staticmethod
    def get_all_metrics():
        """Всі метрики разом"""
        return {
            'articles': BlogMetrics.get_article_metrics(),
            'comments': BlogMetrics.get_comment_metrics(),
            'users': BlogMetrics.get_user_metrics(),
            'requests': request_metrics.get_stats(),
            'timestamp': datetime.now().isoformat(),
        }
