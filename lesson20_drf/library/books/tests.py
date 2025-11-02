from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Book


class BookModelTestCase(TestCase):
    """Тести для моделі Book."""

    def setUp(self):
        """Налаштування тестових даних."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.book = Book.objects.create(
            title='Тестова книга',
            author='Тестовий автор',
            genre='Тестовий жанр',
            publication_year=2023,
            user=self.user
        )

    def test_book_creation(self):
        """Тест створення книги."""
        self.assertEqual(self.book.title, 'Тестова книга')
        self.assertEqual(self.book.author, 'Тестовий автор')
        self.assertEqual(str(self.book), 'Тестова книга (Тестовий автор, 2023)')

    def test_book_user_relation(self):
        """Тест зв'язку книги з користувачем."""
        self.assertEqual(self.book.user, self.user)
        self.assertEqual(self.user.books.count(), 1)


class BookAPITestCase(APITestCase):
    """Тести для API управління книгами."""

    def setUp(self):
        """Налаштування тестових даних та клієнта."""
        # Створення користувачів
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.admin = User.objects.create_user(
            username='admin',
            password='adminpass123',
            email='admin@example.com',
            is_staff=True
        )

        # Створення тестових книг
        self.book1 = Book.objects.create(
            title='Кобзар',
            author='Тарас Шевченко',
            genre='Поезія',
            publication_year=1840,
            user=self.user
        )
        self.book2 = Book.objects.create(
            title='Тіні забутих предків',
            author='Михайло Коцюбинський',
            genre='Новела',
            publication_year=1911,
            user=self.user
        )

        self.client = APIClient()

    def test_get_books_unauthenticated(self):
        """Тест отримання списку книг без аутентифікації."""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_books_authenticated(self):
        """Тест отримання списку книг з аутентифікацією."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_book(self):
        """Тест створення нової книги."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-list')
        data = {
            'title': 'Захар Беркут',
            'author': 'Іван Франко',
            'genre': 'Історична повість',
            'publication_year': 1883
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(response.data['title'], 'Захар Беркут')
        self.assertEqual(response.data['user'], 'testuser')

    def test_get_book_detail(self):
        """Тест отримання деталей книги."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Кобзар')
        self.assertEqual(response.data['author'], 'Тарас Шевченко')

    def test_update_book(self):
        """Тест оновлення книги."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Кобзар (оновлене видання)',
            'author': 'Тарас Шевченко',
            'genre': 'Поезія',
            'publication_year': 1840
        }
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Кобзар (оновлене видання)')

    def test_delete_book_as_user(self):
        """Тест видалення книги звичайним користувачем (має бути заборонено)."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 2)

    def test_delete_book_as_admin(self):
        """Тест видалення книги адміністратором."""
        self.client.force_authenticate(user=self.admin)
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books_by_author(self):
        """Тест фільтрації книг за автором."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-list')
        response = self.client.get(url, {'author': 'Шевченко'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['author'], 'Тарас Шевченко')

    def test_filter_books_by_year_range(self):
        """Тест фільтрації книг за діапазоном років."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-list')
        response = self.client.get(url, {'year_from': 1900, 'year_to': 1920})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Тіні забутих предків')

    def test_search_books(self):
        """Тест пошуку книг за назвою."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Кобзар'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Кобзар')

    def test_order_books_by_year(self):
        """Тест сортування книг за роком видання."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'publication_year'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['publication_year'], 1840)
        self.assertEqual(response.data['results'][1]['publication_year'], 1911)

    def test_my_books_endpoint(self):
        """Тест ендпоінту отримання книг користувача."""
        # Створюємо іншого користувача з його книгою
        other_user = User.objects.create_user(
            username='otheruser',
            password='pass123'
        )
        Book.objects.create(
            title='Інша книга',
            author='Інший автор',
            genre='Інший жанр',
            publication_year=2000,
            user=other_user
        )

        self.client.force_authenticate(user=self.user)
        url = reverse('book-my-books')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Тільки книги поточного користувача

    def test_statistics_endpoint(self):
        """Тест ендпоінту статистики."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-statistics')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_books', response.data)
        self.assertIn('total_authors', response.data)
        self.assertIn('my_books_count', response.data)
        self.assertEqual(response.data['total_books'], 2)
