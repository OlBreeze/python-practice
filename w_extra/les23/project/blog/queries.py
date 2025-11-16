from django.db import connection
from django.db.models import Count, Q, F, Avg, Sum, Max, Min
from .models import Article, Comment, Tag, CustomUser


class ArticleQueries:
    """Клас з кастомними запитами для статей"""

    @staticmethod
    def get_popular_articles_raw(limit=10):
        """
        Отримати популярні статті через raw SQL
        """
        with connection.cursor() as cursor:
            cursor.execute("""
                           SELECT a.id,
                                  a.title,
                                  a.slug,
                                  a.views_count,
                                  u.username           as author_name,
                                  COUNT(DISTINCT c.id) as comment_count
                           FROM blog_article a
                                    INNER JOIN blog_customuser u ON a.author_id = u.id
                                    LEFT JOIN blog_comment c ON a.id = c.article_id AND c.is_approved = TRUE
                           WHERE a.status = 'published'
                           GROUP BY a.id, a.title, a.slug, a.views_count, u.username
                           ORDER BY a.views_count DESC
                               LIMIT %s
                           """, [limit])

            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def get_articles_with_stats():
        """
        Отримати статті зі статистикою через ORM
        """
        return Article.objects.filter(
            status='published'
        ).select_related('author').annotate(
            comment_count=Count('comments', filter=Q(comments__is_approved=True)),
            avg_comment_length=Avg('comments__content'),
            total_views=Sum('views_count'),
        ).order_by('-views_count')

    @staticmethod
    def get_author_statistics_raw(author_id):
        """
        Статистика автора через raw SQL
        """
        with connection.cursor() as cursor:
            cursor.execute("""
                           SELECT COUNT(DISTINCT a.id) as total_articles,
                                  SUM(a.views_count)   as total_views,
                                  COUNT(DISTINCT c.id) as total_comments,
                                  AVG(a.views_count)   as avg_views,
                                  MAX(a.created_at)    as last_published
                           FROM blog_article a
                                    LEFT JOIN blog_comment c ON a.id = c.article_id
                           WHERE a.author_id = %s
                             AND a.status = 'published'
                           """, [author_id])

            row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row)) if row else {}

    @staticmethod
    def get_trending_articles(days=7):
        """
        Трендові статті за останні N днів
        """
        from datetime import timedelta
        from django.utils import timezone

        date_threshold = timezone.now() - timedelta(days=days)

        return Article.objects.filter(
            status='published',
            created_at__gte=date_threshold
        ).annotate(
            comment_count=Count('comments', filter=Q(comments__is_approved=True)),
            engagement_score=F('views_count') + F('comment_count') * 10
        ).order_by('-engagement_score')[:10]

    @staticmethod
    def search_articles_fulltext(query):
        """
        Повнотекстовий пошук через raw SQL (для PostgreSQL)
        """
        with connection.cursor() as cursor:
            cursor.execute("""
                           SELECT id,
                                  title,
                                  slug,
                                  content,
                                  ts_rank(
                                          to_tsvector('english', title || ' ' || content),
                                          plainto_tsquery('english', %s)
                                  ) as rank
                           FROM blog_article
                           WHERE status = 'published'
                             AND (
                               to_tsvector('english', title || ' ' || content) @@
                               plainto_tsquery('english', %s)
                               )
                           ORDER BY rank DESC LIMIT 20
                           """, [query, query])

            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]


class TagQueries:
    """Клас з кастомними запитами для тегів"""

    @staticmethod
    def get_tag_cloud():
        """
        Отримати хмару тегів з кількістю статей
        """
        return Tag.objects.annotate(
            article_count=Count('articles', filter=Q(articles__status='published')),
            total_views=Sum('articles__views_count', filter=Q(articles__status='published'))
        ).filter(article_count__gt=0).order_by('-article_count')

    @staticmethod
    def get_related_tags(tag_id, limit=5):
        """
        Отримати пов'язані теги через raw SQL
        """
        with connection.cursor() as cursor:
            cursor.execute("""
                           SELECT t2.id,
                                  t2.name,
                                  COUNT(DISTINCT a.id) as shared_articles
                           FROM blog_tag t1
                                    INNER JOIN blog_article_tags at1 ON t1.id = at1.tag_id
                                    INNER JOIN blog_article a ON at1.article_id = a.id
                                    INNER JOIN blog_article_tags at2 ON a.id = at2.article_id
                                    INNER JOIN blog_tag t2 ON at2.tag_id = t2.id
                           WHERE t1.id = %s
                             AND t2.id != %s
                             AND a.status = 'published'
                           GROUP BY t2.id, t2.name
                           ORDER BY shared_articles DESC
                               LIMIT %s
                           """, [tag_id, tag_id, limit])

            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]


class CommentQueries:
    """Клас з кастомними запитами для коментарів"""

    @staticmethod
    def get_recent_comments(limit=10):
        """
        Отримати останні коментарі
        """
        return Comment.objects.filter(
            is_approved=True
        ).select_related('author', 'article').order_by('-created_at')[:limit]

    @staticmethod
    def get_most_active_commenters(limit=10):
        """
        Найактивніші коментатори
        """
        return CustomUser.objects.annotate(
            comment_count=Count('comments', filter=Q(comments__is_approved=True))
        ).filter(comment_count__gt=0).order_by('-comment_count')[:limit]

# Використання:
# from blog.queries import ArticleQueries, TagQueries
#
# popular = ArticleQueries.get_popular_articles_raw(10)
# stats = ArticleQueries.get_author_statistics_raw(user_id)
# tags = TagQueries.get_tag_cloud()