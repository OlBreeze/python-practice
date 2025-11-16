from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from .models import Article, Comment, Tag, CustomUser
from .serializers import (
    ArticleListSerializer, ArticleDetailSerializer,
    CommentSerializer, TagSerializer, UserSerializer
)


# ========== Кастомні дозволи ==========
class IsAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    """Дозвіл: автор може редагувати, інші тільки читати"""

    def has_object_permission(self, request, view, obj):
        # Дозвіл на читання для всіх
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Дозвіл на запис тільки для автора
        return obj.author == request.user or request.user.is_staff


class IsOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    """Дозвіл: власник може редагувати"""

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj == request.user or request.user.is_staff


# ========== Пагінація ==========
class StandardResultsSetPagination(PageNumberPagination):
    """Стандартна пагінація"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# ========== ViewSets ==========
class ArticleViewSet(viewsets.ModelViewSet):
    """
    ViewSet для статей з фільтрацією та пошуком

    Фільтри:
    - status: draft, published, archived
    - author: ID автора
    - tags: назва тегу
    - search: пошук по заголовку та контенту
    - ordering: created_at, -created_at, views_count, -views_count
    """

    queryset = Article.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Фільтрація
    filterset_fields = ['status', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'views_count', 'updated_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Різні серіалізатори для списку та деталей"""
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleDetailSerializer

    def get_queryset(self):
        """Оптимізований queryset з фільтрацією"""
        queryset = Article.objects.select_related('author').prefetch_related('tags')

        # Фільтр за тегом
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(tags__name=tag)

        # Фільтр за датою
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)

        # Мінімальна кількість переглядів
        min_views = self.request.query_params.get('min_views')
        if min_views:
            queryset = queryset.filter(views_count__gte=min_views)

        # Тільки опубліковані для неавторизованих
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        elif not self.request.user.is_staff:
            # Користувачі бачать тільки свої статті та опубліковані
            queryset = queryset.filter(
                Q(status='published') | Q(author=self.request.user)
            )

        # Додаємо підрахунок коментарів
        queryset = queryset.annotate(
            comment_count=Count('comments', filter=Q(comments__is_approved=True))
        )

        return queryset.distinct()

    def perform_create(self, serializer):
        """Встановлення автора при створенні"""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        """Збільшити лічильник переглядів"""
        article = self.get_object()
        article.increment_views()
        return Response({'views_count': article.views_count})

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Отримати статистику статті"""
        article = self.get_object()
        return Response(article.get_statistics())

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Найпопулярніші статті"""
        articles = self.get_queryset().filter(
            status='published'
        ).order_by('-views_count')[:10]
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Найновіші статті"""
        articles = self.get_queryset().filter(
            status='published'
        ).order_by('-created_at')[:10]
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для коментарів"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['article', 'author', 'is_approved']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Comment.objects.select_related('author', 'article')

        # Тільки схвалені для неавторизованих
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_approved=True)

        return queryset

    def perform_create(self, serializer):
        """Встановлення автора"""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        """Схвалити коментар (тільки для staff)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Тільки адміністратори можуть схвалювати коментарі'},
                status=status.HTTP_403_FORBIDDEN
            )

        comment = self.get_object()
        comment.is_approved = True
        comment.save()
        return Response({'status': 'approved'})


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для тегів (тільки читання)"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'name'

    def get_queryset(self):
        queryset = Tag.objects.annotate(
            article_count=Count('articles', filter=Q(articles__status='published'))
        ).filter(article_count__gt=0)

        return queryset.order_by('-article_count')

    @action(detail=True, methods=['get'])
    def articles(self, request, name=None):
        """Отримати статті за тегом"""
        tag = self.get_object()
        articles = tag.articles.filter(status='published').select_related('author')

        page = self.paginate_queryset(articles)
        if page is not None:
            serializer = ArticleListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для користувачів"""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_queryset(self):
        return CustomUser.objects.annotate(
            article_count=Count('articles', filter=Q(articles__status='published'))
        )

    @action(detail=True, methods=['get'])
    def articles(self, request, username=None):
        """Отримати статті користувача"""
        user = self.get_object()
        articles = user.articles.filter(status='published').select_related('author')

        page = self.paginate_queryset(articles)
        if page is not None:
            serializer = ArticleListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)