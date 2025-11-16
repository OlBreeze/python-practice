from datetime import datetime
from django.db.models import Count, Q
from .models import Article, Tag, Category


def global_context(request):
    """Глобальний контекстний процесор"""
    return {
        'site_name': 'Мій Блог',
        'current_year': datetime.now().year,
        'recent_articles': Article.objects.filter(
            status='published'
        ).order_by('-created_at')[:5],
        'popular_tags': Tag.objects.annotate(
            article_count=Count('articles', filter=Q(articles__status='published'))
        ).filter(article_count__gt=0).order_by('-article_count')[:10],
        'categories': Category.objects.filter(parent=None),
        'total_articles': Article.objects.filter(status='published').count(),
    }