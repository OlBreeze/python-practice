import pytest
import django
from django.conf import settings

# Налаштування Django перед імпортом моделей
def pytest_configure():
    """Конфігурація pytest для Django"""
    pass  # pytest-django автоматично налаштує Django


@pytest.fixture
def api_user():
    '''Фікстура для створення API користувача'''
    from django.contrib.auth.models import User

    return User.objects.create_user(
        username='apiuser',
        email='api@example.com',
        password='testpass123'
    )


@pytest.fixture
def multiple_users():
    '''Фікстура для створення декількох користувачів'''
    from django.contrib.auth.models import User

    users = []
    for i in range(3):
        users.append(User.objects.create_user(
            username=f'user{i}',
            email=f'user{i}@example.com',
            password=f'password{i}'
        ))
    return users


@pytest.fixture
def sample_task(api_user):
    '''Фікстура для створення тестового завдання'''
    from main.models import Task
    from datetime import date, timedelta

    return Task.objects.create(
        title='Тестове завдання',
        description='Опис тестового завдання',
        due_date=date.today() + timedelta(days=7),
        user=api_user
    )
