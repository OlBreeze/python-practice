# management/commands/populate_db.py
from django.core.management.base import BaseCommand
from myapp.models import Author, Book, Review
import random


class Command(BaseCommand):
    help = 'Заповнює базу даних тестовими даними'

    def handle(self, *args, **kwargs):
        self.stdout.write('Очищення бази даних...')
        Review.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()

        self.stdout.write('Створення авторів...')
        authors = []
        author_names = [
            'Тарас Шевченко', 'Леся Українка', 'Іван Франко',
            'Михайло Коцюбинський', 'Панас Мирний', 'Марко Вовчок',
            'Ольга Кобилянська', 'Василь Стефаник', 'Остап Вишня',
            'Григорій Сковорода'
        ]

        for name in author_names:
            author = Author.objects.create(name=name)
            authors.append(author)

        self.stdout.write('Створення книг...')
        books = []
        book_titles = [
            'Кобзар', 'Лісова пісня', 'Захар Беркут', 'Тіні забутих предків',
            'Повія', 'Маруся', 'Земля', 'Камінний хрест', 'Усмішки',
            'Пісні', 'Intermezzo', 'На полі крові', 'Хіба ревуть воли',
            'Украдене щастя', 'Невольник', 'Сон', 'Енеїда', 'Одержима'
        ]

        for i in range(50):
            book = Book.objects.create(
                title=f'{random.choice(book_titles)} ({i + 1})',
                author=random.choice(authors),
                published_year=random.randint(1850, 2023)
            )
            books.append(book)

        self.stdout.write('Створення відгуків...')
        comments = [
            'Чудова книга!',
            'Дуже цікаво написано',
            'Рекомендую до прочитання',
            'Захоплююча історія',
            'Класика української літератури',
            'Неперевершений твір',
            'Глибокий зміст'
        ]

        for book in books:
            num_reviews = random.randint(5, 20)
            for _ in range(num_reviews):
                Review.objects.create(
                    book=book,
                    rating=random.randint(1, 5),
                    comment=random.choice(comments)
                )

        self.stdout.write(self.style.SUCCESS(
            f'Успішно створено:\n'
            f'- {len(authors)} авторів\n'
            f'- {len(books)} книг\n'
            f'- {Review.objects.count()} відгуків'
        ))