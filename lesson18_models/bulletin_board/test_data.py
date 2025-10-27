"""
Скрипт для створення тестових даних у базі даних.
"""

import os
import django

# Налаштування Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulletin_board.settings')
django.setup()

from django.contrib.auth.models import User
from board.models import Category, Ad, Comment
from decimal import Decimal


def create_test_data():
    """
    Створює тестові дані для демонстрації роботи системи.
    """
    print("Створення тестових даних...")

    # Створення користувачів
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print(f"✓ Створено суперкористувача: {admin.username}")
    else:
        admin = User.objects.get(username='admin')
        print(f"✓ Суперкористувач вже існує: {admin.username}")

    # Створення звичайних користувачів
    users_data = [
        {'username': 'ivan', 'email': 'ivan@example.com', 'password': 'pass123'},
        {'username': 'maria', 'email': 'maria@example.com', 'password': 'pass123'},
        {'username': 'petro', 'email': 'petro@example.com', 'password': 'pass123'},
    ]

    users = []
    for user_data in users_data:
        if not User.objects.filter(username=user_data['username']).exists():
            user = User.objects.create_user(**user_data)
            users.append(user)
            print(f"✓ Створено користувача: {user.username}")
        else:
            user = User.objects.get(username=user_data['username'])
            users.append(user)
            print(f"✓ Користувач вже існує: {user.username}")

    # Оновлення профілів
    admin.profile.phone_number = '+380501111111'
    admin.profile.address = 'Київ, вул. Хрещатик, 1'
    admin.profile.save()

    users[0].profile.phone_number = '+380502222222'
    users[0].profile.address = 'Львів, пр. Свободи, 10'
    users[0].profile.save()

    users[1].profile.phone_number = '+380503333333'
    users[1].profile.address = 'Одеса, вул. Дерибасівська, 5'
    users[1].profile.save()

    print("✓ Оновлено профілі користувачів")

    # Створення категорій
    categories_data = [
        {
            'name': 'Електроніка',
            'description': 'Комп\'ютери, телефони, планшети, техніка'
        },
        {
            'name': 'Транспорт',
            'description': 'Автомобілі, мотоцикли, велосипеди'
        },
        {
            'name': 'Нерухомість',
            'description': 'Квартири, будинки, земельні ділянки'
        },
        {
            'name': 'Меблі',
            'description': 'Меблі для дому та офісу'
        },
        {
            'name': 'Одяг',
            'description': 'Одяг, взуття, аксесуари'
        },
    ]

    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        categories.append(category)
        if created:
            print(f"✓ Створено категорію: {category.name}")
        else:
            print(f"✓ Категорія вже існує: {category.name}")

    # Створення оголошень
    ads_data = [
        {
            'title': 'Продам iPhone 15 Pro',
            'description': 'Новий iPhone 15 Pro 256GB, колір титановий. Повний комплект, гарантія.',
            'price': Decimal('42000.00'),
            'user': users[0],
            'category': categories[0],
        },
        {
            'title': 'Ноутбук MacBook Air M2',
            'description': 'MacBook Air 2023, процесор M2, 16GB RAM, 512GB SSD. Стан ідеальний.',
            'price': Decimal('48000.00'),
            'user': users[0],
            'category': categories[0],
        },
        {
            'title': 'Toyota Camry 2020',
            'description': 'Автомобіль у відмінному стані, один власник, пробіг 45000 км.',
            'price': Decimal('850000.00'),
            'user': users[1],
            'category': categories[1],
        },
        {
            'title': 'Велосипед гірський',
            'description': 'Гірський велосипед Trek, 21 швидкість, алюмінієва рама.',
            'price': Decimal('12000.00'),
            'user': users[1],
            'category': categories[1],
        },
        {
            'title': '2-кімнатна квартира в центрі',
            'description': 'Квартира 65 кв.м., 5/9 поверх, євроремонт, всі зручності.',
            'price': Decimal('2500000.00'),
            'user': users[2],
            'category': categories[2],
        },
        {
            'title': 'Диван-ліжко IKEA',
            'description': 'Диван-ліжко в ідеальному стані, механізм справний, оббивка без дефектів.',
            'price': Decimal('8500.00'),
            'user': users[2],
            'category': categories[3],
        },
        {
            'title': 'Офісний стіл',
            'description': 'Стіл для офісу або домашньої роботи, розмір 140x80 см.',
            'price': Decimal('3200.00'),
            'user': admin,
            'category': categories[3],
        },
        {
            'title': 'Куртка зимова',
            'description': 'Жіноча зимова куртка, розмір M, колір чорний, пуховик.',
            'price': Decimal('2800.00'),
            'user': admin,
            'category': categories[4],
        },
    ]

    created_ads = []
    for ad_data in ads_data:
        if not Ad.objects.filter(title=ad_data['title']).exists():
            ad = Ad.objects.create(**ad_data)
            created_ads.append(ad)
            print(f"✓ Створено оголошення: {ad.title}")
        else:
            ad = Ad.objects.get(title=ad_data['title'])
            created_ads.append(ad)
            print(f"✓ Оголошення вже існує: {ad.title}")

    # Створення коментарів
    comments_data = [
        {
            'content': 'Дуже цікаве оголошення! Скільки років використання?',
            'ad': created_ads[0],
            'user': users[1],
        },
        {
            'content': 'Можлива знижка при швидкому викупі?',
            'ad': created_ads[0],
            'user': users[2],
        },
        {
            'content': 'Чудовий ноутбук! Коли можна подивитися?',
            'ad': created_ads[1],
            'user': users[2],
        },
        {
            'content': 'Автомобіль на ходу? Чи були ДТП?',
            'ad': created_ads[2],
            'user': users[0],
        },
        {
            'content': 'Дуже гарна квартира! Чи можна оглянути у вихідні?',
            'ad': created_ads[4],
            'user': users[0],
        },
    ]

    for comment_data in comments_data:
        if not Comment.objects.filter(
                content=comment_data['content'],
                ad=comment_data['ad']
        ).exists():
            comment = Comment.objects.create(**comment_data)
            print(f"✓ Створено коментар до: {comment.ad.title}")
        else:
            print(f"✓ Коментар вже існує")

    print("\n" + "=" * 60)
    print("Тестові дані успішно створено!")
    print("=" * 60)
    print(f"\nКатегорій: {Category.objects.count()}")
    print(f"Оголошень: {Ad.objects.count()}")
    print(f"Коментарів: {Comment.objects.count()}")
    print(f"\nЗапустіть сервер: python manage.py runserver")
    print(f"Відкрийте у браузері: http://127.0.0.1:8000")
    print("=" * 60)


if __name__ == '__main__':
    create_test_data()
