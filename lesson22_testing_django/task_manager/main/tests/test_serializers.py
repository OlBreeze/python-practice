import pytest
from datetime import date, timedelta
from django.contrib.auth.models import User
from main.serializers import TaskSerializer
from main.models import Task


# ООП ПІДХІД
@pytest.mark.django_db
class TestTaskSerializerOOP:
    """Тестування TaskSerializer з використанням ООП"""

    @pytest.fixture(autouse=True)
    def setup(self, db):
        """Підготовка даних перед кожним тестом"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.valid_data = {
            'title': 'Тестове завдання API',
            'description': 'Опис завдання для API',
            'due_date': str(date.today() + timedelta(days=7)),
            'user': self.user.id
        }

    def test_serializer_valid_with_correct_data(self):
        """Перевірка валідності серіалізатора з правильними даними"""
        serializer = TaskSerializer(data=self.valid_data)
        assert serializer.is_valid(), f"Помилки: {serializer.errors}"
        assert serializer.validated_data['title'] == self.valid_data['title']

    def test_serializer_invalid_without_title(self):
        """Перевірка помилок при відсутності обов'язкового поля title"""
        data = self.valid_data.copy()
        del data['title']
        serializer = TaskSerializer(data=data)
        assert not serializer.is_valid()
        assert 'title' in serializer.errors

    def test_serializer_invalid_with_empty_title(self):
        """Перевірка помилок при пустому title"""
        data = self.valid_data.copy()
        data['title'] = ''
        serializer = TaskSerializer(data=data)
        assert not serializer.is_valid()
        assert 'title' in serializer.errors

    def test_serializer_custom_validation_past_date(self):
        """Перевірка кастомної валідації для минулої дати"""
        data = self.valid_data.copy()
        data['due_date'] = str(date.today() - timedelta(days=1))
        serializer = TaskSerializer(data=data)
        assert not serializer.is_valid()
        assert 'due_date' in serializer.errors
        assert 'минулому' in str(serializer.errors['due_date'][0]).lower()

    def test_serializer_valid_with_today_date(self):
        """Перевірка валідності з сьогоднішньою датою"""
        data = self.valid_data.copy()
        data['due_date'] = str(date.today())
        serializer = TaskSerializer(data=data)
        assert serializer.is_valid()

    def test_serializer_create_task(self):
        """Перевірка створення задачі через серіалізатор"""
        serializer = TaskSerializer(data=self.valid_data)
        assert serializer.is_valid()
        task = serializer.save()
        assert task.title == self.valid_data['title']
        assert task.user == self.user
        assert Task.objects.filter(id=task.id).exists()

    def test_serializer_update_task(self):
        """Перевірка оновлення задачі через серіалізатор"""
        task = Task.objects.create(
            title='Старий заголовок',
            description='Старий опис',
            due_date=date.today() + timedelta(days=5),
            user=self.user
        )

        update_data = {
            'title': 'Новий заголовок',
            'description': 'Новий опис',
            'due_date': str(date.today() + timedelta(days=10)),
            'user': self.user.id
        }

        serializer = TaskSerializer(task, data=update_data)
        assert serializer.is_valid()
        updated_task = serializer.save()
        assert updated_task.title == 'Новий заголовок'

    def test_serializer_read_only_fields(self):
        """Перевірка read-only полів"""
        task = Task.objects.create(
            title='Тестове завдання',
            description='Опис',
            due_date=date.today() + timedelta(days=5),
            user=self.user
        )
        serializer = TaskSerializer(task)
        assert 'id' in serializer.data
        assert serializer.data['id'] == task.id


# ФУНКЦІОНАЛЬНИЙ ПІДХІД
@pytest.fixture
def user_fixture():
    """Фікстура для створення користувача"""
    return User.objects.create_user(
        username='funcuser',
        email='func@example.com',
        password='funcpass123'
    )


@pytest.fixture
def valid_task_data(user_fixture):
    """Фікстура для валідних даних завдання"""
    return {
        'title': 'Функціональне завдання',
        'description': 'Опис',
        'due_date': str(date.today() + timedelta(days=5)),
        'user': user_fixture.id
    }


@pytest.mark.django_db
def test_serializer_valid_functional(valid_task_data):
    """Функціональний тест валідності серіалізатора"""
    serializer = TaskSerializer(data=valid_task_data)
    assert serializer.is_valid()


@pytest.mark.django_db
@pytest.mark.parametrize("field_to_remove", ['title', 'description', 'due_date', 'user'])
def test_serializer_missing_fields_functional(valid_task_data, field_to_remove):
    """Параметризований тест для перевірки відсутніх полів"""
    data = valid_task_data.copy()
    del data[field_to_remove]
    serializer = TaskSerializer(data=data)
    assert not serializer.is_valid()
    assert field_to_remove in serializer.errors


@pytest.mark.django_db
@pytest.mark.parametrize("days_offset,should_be_valid", [
    (-5, False),
    (-1, False),
    (0, True),
    (1, True),
    (10, True),
    (365, True),
])
def test_serializer_date_validation_functional(valid_task_data, days_offset, should_be_valid):
    """Параметризований тест для валідації дат в серіалізаторі"""
    data = valid_task_data.copy()
    data['due_date'] = str(date.today() + timedelta(days=days_offset))
    serializer = TaskSerializer(data=data)
    assert serializer.is_valid() == should_be_valid


@pytest.mark.django_db
def test_serializer_create_and_retrieve_functional(valid_task_data, user_fixture):
    """Функціональний тест створення та отримання завдання"""
    # Створення
    serializer = TaskSerializer(data=valid_task_data)
    assert serializer.is_valid()
    task = serializer.save()

    # Отримання
    retrieved_serializer = TaskSerializer(task)
    assert retrieved_serializer.data['title'] == valid_task_data['title']
    assert retrieved_serializer.data['user'] == user_fixture.id

