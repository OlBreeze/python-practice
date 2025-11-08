import pytest
from datetime import date, timedelta
from django.contrib.auth.models import User
from main.serializers import TaskWithUserSerializer
from main.models import Task


# ============================================================================
# ООП ПІДХІД
# ============================================================================

@pytest.mark.django_db
class TestTaskWithUserSerializerOOP:
    """Тестування вкладеного серіалізатора з використанням ООП"""

    def setup_method(self):
        """Підготовка даних"""
        self.valid_data = {
            'title': 'Завдання з користувачем',
            'description': 'Опис завдання',
            'due_date': str(date.today() + timedelta(days=7)),
            'user': {
                'username': 'nesteduser',
                'email': 'nested@example.com',
                'first_name': 'Тест',
                'last_name': 'Користувач'
            }
        }

    def test_nested_serializer_valid_with_correct_data(self):
        """Перевірка валідності вкладеного серіалізатора"""
        serializer = TaskWithUserSerializer(data=self.valid_data)
        assert serializer.is_valid(), f"Помилки: {serializer.errors}"
        assert serializer.validated_data['title'] == self.valid_data['title']
        assert serializer.validated_data['user']['username'] == self.valid_data['user']['username']

    def test_nested_serializer_invalid_empty_username(self):
        """Перевірка помилок при пустому username"""
        data = self.valid_data.copy()
        data['user'] = self.valid_data['user'].copy()
        data['user']['username'] = ''
        serializer = TaskWithUserSerializer(data=data)
        assert not serializer.is_valid()
        assert 'user' in serializer.errors

    def test_nested_serializer_missing_user_username(self):
        """Перевірка помилок при відсутності username користувача"""
        data = self.valid_data.copy()
        data['user'] = self.valid_data['user'].copy()
        del data['user']['username']
        serializer = TaskWithUserSerializer(data=data)
        assert not serializer.is_valid()
        assert 'user' in serializer.errors

    def test_nested_serializer_invalid_email(self):
        """Перевірка валідації email користувача"""
        data = self.valid_data.copy()
        data['user'] = self.valid_data['user'].copy()
        data['user']['email'] = 'not-an-email'
        serializer = TaskWithUserSerializer(data=data)
        assert not serializer.is_valid()
        assert 'user' in serializer.errors

    def test_nested_serializer_missing_user_data(self):
        """Перевірка помилок при відсутності даних користувача"""
        data = self.valid_data.copy()
        del data['user']
        serializer = TaskWithUserSerializer(data=data)
        assert not serializer.is_valid()
        assert 'user' in serializer.errors

    def test_nested_serializer_create_with_user(self):
        """Перевірка створення завдання з користувачем"""
        serializer = TaskWithUserSerializer(data=self.valid_data)
        assert serializer.is_valid()
        task = serializer.save()
        assert task.title == self.valid_data['title']
        assert task.user.username == self.valid_data['user']['username']
        assert User.objects.filter(username='nesteduser').exists()

    def test_nested_serializer_read_existing_task(self):
        """Перевірка читання існуючого завдання з користувачем"""
        user = User.objects.create_user(
            username='readuser',
            email='read@example.com'
        )
        task = Task.objects.create(
            title='Існуюче завдання',
            description='Опис',
            due_date=date.today() + timedelta(days=5),
            user=user
        )
        serializer = TaskWithUserSerializer(task)
        assert serializer.data['title'] == task.title
        assert serializer.data['user']['username'] == user.username

    def test_nested_serializer_past_date_validation(self):
        """Перевірка валідації минулої дати у вкладеному серіалізаторі"""
        data = self.valid_data.copy()
        data['due_date'] = str(date.today() - timedelta(days=1))
        serializer = TaskWithUserSerializer(data=data)
        assert not serializer.is_valid()
        assert 'due_date' in serializer.errors


# ============================================================================
# ФУНКЦІОНАЛЬНИЙ ПІДХІД
# ============================================================================

@pytest.fixture
def valid_nested_data():
    """Фікстура для валідних вкладених даних"""
    return {
        'title': 'Функціональне вкладене завдання',
        'description': 'Опис',
        'due_date': str(date.today() + timedelta(days=3)),
        'user': {
            'username': 'funcnesteduser',
            'email': 'funcnested@example.com',
            'first_name': 'Функція',
            'last_name': 'Тест'
        }
    }


@pytest.mark.django_db
def test_nested_serializer_valid_functional(valid_nested_data):
    """Функціональний тест валідності вкладеного серіалізатора"""
    serializer = TaskWithUserSerializer(data=valid_nested_data)
    assert serializer.is_valid()
    task = serializer.save()
    assert task.user.username == valid_nested_data['user']['username']


@pytest.mark.django_db
@pytest.mark.parametrize("user_field,invalid_value", [
    ('username', ''),
    ('email', 'invalid-email'),
    ('email', ''),
])
def test_nested_serializer_invalid_user_fields_functional(valid_nested_data, user_field, invalid_value):
    """Параметризований тест для невалідних полів користувача"""
    data = valid_nested_data.copy()
    data['user'] = valid_nested_data['user'].copy()
    data['user'][user_field] = invalid_value
    serializer = TaskWithUserSerializer(data=data)
    assert not serializer.is_valid()
    assert 'user' in serializer.errors


@pytest.mark.django_db
def test_nested_serializer_missing_user_data_functional(valid_nested_data):
    """Функціональний тест відсутності даних користувача"""
    data = valid_nested_data.copy()
    del data['user']
    serializer = TaskWithUserSerializer(data=data)
    assert not serializer.is_valid()
    assert 'user' in serializer.errors


@pytest.mark.django_db
@pytest.mark.parametrize("missing_field", ['username', 'email'])
def test_nested_serializer_missing_user_fields_functional(valid_nested_data, missing_field):
    """Параметризований тест для відсутніх полів користувача"""
    data = valid_nested_data.copy()
    data['user'] = valid_nested_data['user'].copy()
    del data['user'][missing_field]
    serializer = TaskWithUserSerializer(data=data)
    assert not serializer.is_valid()
    assert 'user' in serializer.errors


@pytest.mark.django_db
def test_nested_serializer_full_workflow_functional(valid_nested_data):
    """Функціональний тест повного робочого процесу"""
    # Створення
    serializer = TaskWithUserSerializer(data=valid_nested_data)
    assert serializer.is_valid()
    task = serializer.save()

    # Перевірка створення
    assert Task.objects.filter(id=task.id).exists()
    assert User.objects.filter(username=valid_nested_data['user']['username']).exists()

    # Читання
    read_serializer = TaskWithUserSerializer(task)
    assert read_serializer.data['title'] == valid_nested_data['title']
    assert read_serializer.data['user']['username'] == valid_nested_data['user']['username']
