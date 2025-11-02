from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Book
from .serializers import BookSerializer, BookListSerializer
from .filters import BookFilter
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управління книгами.

    Надає наступні ендпоінти:
    - GET /api/books/ - список всіх книг (з пагінацією, фільтрацією та пошуком)
    - POST /api/books/ - створення нової книги
    - GET /api/books/{id}/ - деталі окремої книги
    - PUT /api/books/{id}/ - повне оновлення книги
    - PATCH /api/books/{id}/ - часткове оновлення книги
    - DELETE /api/books/{id}/ - видалення книги (тільки для адміністраторів)
    - GET /api/books/my_books/ - книги поточного користувача
    - GET /api/books/statistics/ - статистика по книгах

    Фільтрація:
    - author: фільтрація за автором
    - genre: фільтрація за жанром
    - publication_year: фільтрація за роком видання
    - year_from: книги від вказаного року
    - year_to: книги до вказаного року

    Пошук:
    - search: пошук за назвою або автором

    Сортування:
    - ordering: сортування за полями (title, author, publication_year, created_at)
      Для зворотного сортування використовуйте '-' перед полем (наприклад, -publication_year)
    """
    queryset = Book.objects.select_related('user').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author']
    ordering_fields = ['title', 'author', 'publication_year', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """
        Повертає відповідний серіалізатор в залежності від дії.

        Returns:
            BookListSerializer для списку книг
            BookSerializer для деталей та операцій створення/оновлення
        """
        if self.action == 'list':
            return BookListSerializer
        return BookSerializer

    def perform_create(self, serializer):
        """
        Зберігає нову книгу з поточним користувачем як власником.

        Args:
            serializer: Серіалізатор з валідованими даними
        """
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Отримати список книг поточного користувача",
        responses={200: BookSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def my_books(self, request):
        """
        Повертає список книг, створених поточним користувачем.

        Args:
            request: HTTP запит

        Returns:
            Response зі списком книг користувача
        """
        books = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Отримати статистику по книгах",
        responses={
            200: openapi.Response(
                description="Статистика",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_books': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_authors': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_genres': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'my_books_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                    }
                )
            )
        }
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Повертає статистику по всіх книгах.

        Args:
            request: HTTP запит

        Returns:
            Response зі статистикою
        """
        total_books = self.queryset.count()
        total_authors = self.queryset.values('author').distinct().count()
        total_genres = self.queryset.values('genre').distinct().count()
        my_books = self.queryset.filter(user=request.user).count()

        return Response({
            'total_books': total_books,
            'total_authors': total_authors,
            'total_genres': total_genres,
            'my_books_count': my_books,
        })

# ----------------------------------------------------------------
# Отличный вопрос, Ольга 🌟 —
# ты как раз подошла к **самой "магии" Django REST Framework** — всё это действительно не прописано вручную, потому что DRF **создаёт эти ендпоинты автоматически** 🚀
#
# ## ⚙️ 1. Почему `BookViewSet` сам создаёт эндпоинты
#
# Ты используешь:
#
# ```python
# class BookViewSet(viewsets.ModelViewSet):
# ```
#
# `ModelViewSet` — это "умный" класс, который **комбинирует** все базовые CRUD операции (Create, Read, Update, Delete).
# Он наследуется от нескольких классов:
#
# ```python
# CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet
# ```
#
# И каждый из этих миксинов добавляет свой метод, а значит — свой эндпоинт.
#
# ---
#
# ## 📚 2. Какие методы создаются автоматически
#
# | HTTP метод | URL шаблон         | Метод ViewSet      | Что делает                   |
# | ---------- | ------------------ | ------------------ | ---------------------------- |
# | `GET`      | `/api/books/`      | `list()`           | Повертає список усіх книг    |
# | `POST`     | `/api/books/`      | `create()`         | Створює нову книгу           |
# | `GET`      | `/api/books/{id}/` | `retrieve()`       | Повертає деталі однієї книги |
# | `PUT`      | `/api/books/{id}/` | `update()`         | Повне оновлення книги        |
# | `PATCH`    | `/api/books/{id}/` | `partial_update()` | Часткове оновлення           |
# | `DELETE`   | `/api/books/{id}/` | `destroy()`        | Видаляє книгу                |
#
# 👉 Эти методы DRF добавляет **автоматически**, когда ты используешь `ModelViewSet`.
#
# ---
#
# ## 🧭 3. Откуда берутся URL `/api/books/...`
#
# Они создаются с помощью **роутера** в `urls.py`.
# Например, у тебя должно быть что-то вроде:
#
# ```python
# from rest_framework.routers import DefaultRouter
# from .views import BookViewSet
#
# router = DefaultRouter()
# router.register(r'books', BookViewSet, basename='book')
#
# urlpatterns = [
#     path('api/', include(router.urls)),
# ]
# ```
#
# 🔹 `DefaultRouter` автоматически генерирует все стандартные маршруты для CRUD
# (и даже добавляет `/api/books/` и `/api/books/{id}/` сам).
#
# ---
#
# ## 🧩 4. А откуда берутся `/api/books/my_books/` и `/api/books/statistics/`?
#
# Это **дополнительные действия (custom actions)**, которые ты сама определила:
#
# ```python
# @action(detail=False, methods=['get'])
# def my_books(self, request):
#     ...
# ```
#
# и
#
# ```python
# @action(detail=False, methods=['get'])
# def statistics(self, request):
#     ...
# ```
#
# DRF автоматически превращает их в эндпоинты:
#
# | URL                      | Метод | Метод ViewSet  | Описание                    |
# | ------------------------ | ----- | -------------- | --------------------------- |
# | `/api/books/my_books/`   | GET   | `my_books()`   | Книги текущего пользователя |
# | `/api/books/statistics/` | GET   | `statistics()` | Статистика по книгам        |
#
# 🧠 потому что:
#
# * `@action(detail=False)` → означает, что **эндпоинт не требует ID** (глобальный уровень);
# * если бы ты написала `detail=True`, эндпоинт выглядел бы так: `/api/books/{id}/your_action/`.
#
# ---
#
# ## 🧠 5. Что в итоге создаётся
#
# Когда ты подключаешь этот ViewSet через `router.register('books', BookViewSet)`,
# DRF создаёт автоматически:
#
# ```
# /api/books/               → list(), create()
# /api/books/{id}/          → retrieve(), update(), partial_update(), destroy()
# /api/books/my_books/      → my_books()
# /api/books/statistics/    → statistics()
# ```
#
# И Swagger (`drf_yasg`) красиво покажет их все — с описаниями и примерами.
#
# ---
