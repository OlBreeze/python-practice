# blog/templatetags/blog_tags.py
from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import Count, Q
from datetime import datetime, timedelta
import re

register = template.Library()


# ========== ЗАВДАННЯ 4: Кастомні теги шаблонів ==========

@register.simple_tag
def get_popular_articles(count=5):
    """Отримати найпопулярніші статті"""
    from blog.models import Article
    return Article.objects.filter(
        status='published'
    ).order_by('-views_count')[:count]


@register.simple_tag
def get_recent_articles(count=5):
    """Отримати найновіші статті"""
    from blog.models import Article
    return Article.objects.filter(
        status='published'
    ).order_by('-created_at')[:count]


@register.simple_tag
def get_articles_by_tag(tag_name, count=10):
    """Отримати статті за тегом"""
    from blog.models import Article
    return Article.objects.filter(
        tags__name=tag_name,
        status='published'
    ).distinct()[:count]


@register.simple_tag
def get_article_stats():
    """Отримати загальну статистику блогу"""
    from blog.models import Article, Comment, CustomUser

    total_articles = Article.objects.filter(status='published').count()
    total_comments = Comment.objects.filter(is_approved=True).count()
    total_views = Article.objects.filter(
        status='published'
    ).aggregate(total=Count('views_count'))['total'] or 0
    total_authors = CustomUser.objects.filter(
        articles__status='published'
    ).distinct().count()

    return {
        'total_articles': total_articles,
        'total_comments': total_comments,
        'total_views': total_views,
        'total_authors': total_authors,
    }


@register.simple_tag(takes_context=True)
def query_string(context, **kwargs):
    """Генерувати query string для пагінації з фільтрами"""
    query = context['request'].GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            query[key] = value
        elif key in query:
            del query[key]
    return query.urlencode()


@register.inclusion_tag('blog/tags/article_card.html')
def render_article_card(article, show_excerpt=True):
    """Рендерити картку статті"""
    return {
        'article': article,
        'show_excerpt': show_excerpt,
        'reading_time': article.get_reading_time(),
    }


@register.inclusion_tag('blog/tags/popular_tags.html')
def show_popular_tags(count=10):
    """Відобразити популярні теги"""
    from blog.models import Tag

    tags = Tag.objects.annotate(
        article_count=Count('articles', filter=Q(articles__status='published'))
    ).filter(article_count__gt=0).order_by('-article_count')[:count]

    return {'tags': tags}


@register.inclusion_tag('blog/tags/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    """Відобразити хлібні крихти"""
    return {
        'request': context['request'],
        'breadcrumbs': context.get('breadcrumbs', []),
    }


# ========== ЗАВДАННЯ 4: Кастомні фільтри шаблонів ==========

@register.filter
def reading_time(text):
    """Розрахувати час читання тексту"""
    words = len(text.split())
    minutes = words / 200  # Середня швидкість читання
    return max(1, round(minutes))


@register.filter
def truncate_words(text, length=50):
    """Обрізати текст до певної кількості слів"""
    words = text.split()
    if len(words) <= length:
        return text
    return ' '.join(words[:length]) + '...'


@register.filter
def markdown_to_html(text):
    """Простий конвертер Markdown в HTML"""
    # Заголовки
    text = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)

    # Жирний текст
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.*?)__', r'<strong>\1</strong>', text)

    # Курсив
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.*?)_', r'<em>\1</em>', text)

    # Посилання
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)

    # Параграфи
    paragraphs = text.split('\n\n')
    text = ''.join([f'<p>{p}</p>' for p in paragraphs if p.strip()])

    return mark_safe(text)


@register.filter
def highlight_search(text, query):
    """Підсвітити пошуковий запит у тексті"""
    if not query:
        return text

    pattern = re.compile(re.escape(query), re.IGNORECASE)
    highlighted = pattern.sub(
        lambda m: f'<mark>{m.group(0)}</mark>',
        text
    )
    return mark_safe(highlighted)


@register.filter
def format_number(value):
    """Форматувати число (1000 -> 1K, 1000000 -> 1M)"""
    try:
        value = int(value)
        if value >= 1000000:
            return f'{value / 1000000:.1f}M'
        if value >= 1000:
            return f'{value / 1000:.1f}K'
        return str(value)
    except (ValueError, TypeError):
        return value


@register.filter
def time_since_short(date):
    """Короткий формат часу (2д, 3г, 5хв)"""
    if not date:
        return ''

    now = datetime.now(date.tzinfo) if date.tzinfo else datetime.now()
    diff = now - date

    seconds = diff.total_seconds()

    if seconds < 60:
        return 'щойно'
    elif seconds < 3600:
        return f'{int(seconds / 60)}хв'
    elif seconds < 86400:
        return f'{int(seconds / 3600)}г'
    elif seconds < 604800:
        return f'{int(seconds / 86400)}д'
    elif seconds < 2592000:
        return f'{int(seconds / 604800)}т'
    else:
        return f'{int(seconds / 2592000)}міс'


@register.filter
def status_badge(status):
    """Генерувати HTML badge для статусу"""
    badges = {
        'draft': '<span class="badge badge-warning">Чернетка</span>',
        'published': '<span class="badge badge-success">Опубліковано</span>',
        'archived': '<span class="badge badge-secondary">Архів</span>',
    }
    return mark_safe(badges.get(status, status))


@register.filter
def pluralize_ua(value, forms):
    """Українська плюралізація (1 стаття, 2 статті, 5 статей)"""
    try:
        value = int(value)
        forms = forms.split(',')

        if len(forms) != 3:
            return forms[0] if forms else ''

        if value % 10 == 1 and value % 100 != 11:
            return forms[0]
        elif 2 <= value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20):
            return forms[1]
        else:
            return forms[2]
    except (ValueError, TypeError):
        return forms.split(',')[0] if forms else ''


@register.filter
def add_class(field, css_class):
    """Додати CSS клас до поля форми"""
    return field.as_widget(attrs={'class': css_class})


@register.filter
def get_item(dictionary, key):
    """Отримати елемент зі словника за ключем"""
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def percentage(value, total):
    """Розрахувати відсоток"""
    try:
        value = float(value)
        total = float(total)
        if total == 0:
            return 0
        return round((value / total) * 100, 1)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


# ========== ЗАВДАННЯ 4: Кастомний контекстний процесор ==========
# Додати в settings.py:
# TEMPLATES[0]['OPTIONS']['context_processors'] += [
#     'blog.context_processors.global_context',
# ]

# blog/context_processors.py
def global_context(request):
    """Глобальний контекстний процесор"""
    from blog.models import Article, Tag, Category

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