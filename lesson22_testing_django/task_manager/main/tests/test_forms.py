import pytest
from datetime import date, timedelta

from main.forms import TaskForm


# ООП ПІДХІД
@pytest.mark.django_db
class TestTaskFormOOP:
    """Тестування форми TaskForm з використанням ООП"""

    def setup_method(self):
        """Підготовка даних перед кожним тестом"""
        self.valid_data = {
            'title': 'Тестове завдання',
            'description': 'Опис тестового завдання',
            'due_date': date.today() + timedelta(days=7)
        }

    def test_form_valid_with_correct_data(self):
        """Перевірка валідності форми з правильними даними"""
        form = TaskForm(data=self.valid_data)
        assert form.is_valid(), f"Форма має бути валідною. Помилки: {form.errors}"
        assert form.cleaned_data['title'] == self.valid_data['title']
        assert form.cleaned_data['description'] == self.valid_data['description']
        assert form.cleaned_data['due_date'] == self.valid_data['due_date']

    def test_form_invalid_with_empty_title(self):
        """Перевірка помилок при пустому title"""
        data = self.valid_data.copy()
        data['title'] = ''
        form = TaskForm(data=data)
        assert not form.is_valid()
        assert 'title' in form.errors

    def test_form_invalid_with_empty_description(self):
        """Перевірка помилок при пустому description"""
        data = self.valid_data.copy()
        data['description'] = ''
        form = TaskForm(data=data)
        assert not form.is_valid()
        assert 'description' in form.errors

    def test_form_invalid_with_empty_due_date(self):
        """Перевірка помилок при пустому due_date"""
        data = self.valid_data.copy()
        data['due_date'] = None
        form = TaskForm(data=data)
        assert not form.is_valid()
        assert 'due_date' in form.errors

    def test_form_invalid_with_past_date(self):
        """Перевірка валідації дати в минулому"""
        data = self.valid_data.copy()
        data['due_date'] = date.today() - timedelta(days=1)
        form = TaskForm(data=data)
        assert not form.is_valid()
        assert 'due_date' in form.errors
        assert 'минулому' in str(form.errors['due_date'][0]).lower()

    def test_form_valid_with_today_date(self):
        """Перевірка валідності форми з сьогоднішньою датою"""
        data = self.valid_data.copy()
        data['due_date'] = date.today()
        form = TaskForm(data=data)
        assert form.is_valid()

    def test_form_valid_with_future_date(self):
        """Перевірка валідності форми з майбутньою датою"""
        data = self.valid_data.copy()
        data['due_date'] = date.today() + timedelta(days=30)
        form = TaskForm(data=data)
        assert form.is_valid()


# ФУНКЦІОНАЛЬНИЙ ПІДХІД

@pytest.mark.django_db
def test_task_form_valid_functional():
    """Функціональний тест валідності форми"""
    data = {
        'title': 'Функціональне завдання',
        'description': 'Опис функціонального завдання',
        'due_date': date.today() + timedelta(days=5)
    }
    form = TaskForm(data=data)
    assert form.is_valid()


@pytest.mark.django_db
@pytest.mark.parametrize("field_name", ['title', 'description', 'due_date'])
def test_task_form_required_fields_functional(field_name):
    """Параметризований тест для перевірки обов'язкових полів"""
    data = {
        'title': 'Завдання',
        'description': 'Опис',
        'due_date': date.today() + timedelta(days=1)
    }
    data[field_name] = '' if field_name != 'due_date' else None
    form = TaskForm(data=data)
    assert not form.is_valid()
    assert field_name in form.errors


@pytest.mark.django_db
@pytest.mark.parametrize("days_offset,expected_valid", [
    (-1, False),   # Вчора
    (-7, False),   # Минулий тиждень
    (-30, False),  # Минулий місяць
    (0, True),     # Сьогодні
    (1, True),     # Завтра
    (7, True),     # Наступний тиждень
    (30, True),    # Наступний місяць
])
def test_task_form_date_validation_functional(days_offset, expected_valid):
    """Параметризований тест для валідації дат"""
    data = {
        'title': 'Завдання',
        'description': 'Опис',
        'due_date': date.today() + timedelta(days=days_offset)
    }
    form = TaskForm(data=data)
    assert form.is_valid() == expected_valid


@pytest.mark.django_db
@pytest.mark.parametrize("title,description,is_valid", [
    ("Valid Title", "Valid Description", True),
    ("T", "D", True),  # Мінімальна довжина
    ("T" * 200, "D" * 1000, True),  # Максимальна довжина
    ("", "Valid Description", False),  # Пустий title
    ("Valid Title", "", False),  # Пустий description
])
def test_task_form_field_combinations_functional(title, description, is_valid):
    """Параметризований тест для різних комбінацій полів"""
    data = {
        'title': title,
        'description': description,
        'due_date': date.today() + timedelta(days=1)
    }
    form = TaskForm(data=data)
    assert form.is_valid() == is_valid
