# test_pytest_examples.py
# Установка: pip install pytest

import pytest
from example_1 import add, factorial, divide, is_even


# Простые тесты (без класса)
def test_add_simple():
    """Простой тест сложения"""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_factorial_simple():
    """Простой тест факториала"""
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120


# Тесты исключений в pytest
def test_factorial_negative():
    """Тест исключения для отрицательного числа"""
    with pytest.raises(ValueError):
        factorial(-1)

    # Можно проверить сообщение исключения
    with pytest.raises(ValueError, match="n must be positive"):
        factorial(-5)


def test_divide_by_zero():
    """Тест деления на ноль"""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)


# Параметризованные тесты в pytest
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (10, -5, 5),
    (2.5, 1.5, 4.0)
])
def test_add_parametrized(a, b, expected):
    """Параметризованный тест сложения"""
    assert add(a, b) == expected


@pytest.mark.parametrize("n,expected", [
    (0, 1),
    (1, 1),
    (2, 2),
    (3, 6),
    (4, 24),
    (5, 120)
])
def test_factorial_parametrized(n, expected):
    """Параметризованный тест факториала"""
    assert factorial(n) == expected


# Фикстуры в pytest
@pytest.fixture
def sample_data():
    """Фикстура с тестовыми данными"""
    return [1, 2, 3, 4, 5]


@pytest.fixture
def user_data():
    """Фикстура с данными пользователя"""
    return {
        'name': 'John',
        'age': 25,
        'email': 'john@example.com'
    }


def test_with_fixture(sample_data):
    """Тест использующий фикстуру"""
    assert len(sample_data) == 5
    assert 3 in sample_data
    assert sample_data[0] == 1


def test_user_fixture(user_data):
    """Тест с фикстурой пользователя"""
    assert user_data['name'] == 'John'
    assert user_data['age'] == 25
    assert 'email' in user_data


# Классы тестов в pytest (аналог unittest)
class TestMathOperations:
    """Класс тестов математических операций"""

    def test_add_in_class(self):
        """Тест сложения в классе"""
        assert add(2, 3) == 5

    def test_is_even_in_class(self):
        """Тест проверки четности в классе"""
        assert is_even(4) == True
        assert is_even(3) == False
        assert is_even(0) == True


# Маркеры для группировки тестов
@pytest.mark.slow
def test_slow_operation():
    """Тест помеченный как медленный"""
    import time
    time.sleep(0.1)
    assert True


@pytest.mark.integration
def test_integration():
    """Интеграционный тест"""
    assert True


@pytest.mark.unit
def test_unit():
    """Юнит тест"""
    assert add(1, 1) == 2


# Скип тестов
@pytest.mark.skip(reason="Тест временно отключен")
def test_skipped():
    """Этот тест будет пропущен"""
    assert False


@pytest.mark.skipif(condition=True, reason="Условие выполнено")
def test_conditional_skip():
    """Тест пропускается по условию"""
    assert False


# Ожидание падения теста
@pytest.mark.xfail(reason="Известная ошибка")
def test_expected_failure():
    """Тест который должен упасть"""
    assert False


# Использование approximation для чисел с плавающей точкой
def test_float_approximation():
    """Тест приблизительного равенства"""
    result = divide(10, 3)
    assert result == pytest.approx(3.333333, abs=1e-5)


# Тест с временными файлами
def test_with_tmp_path(tmp_path):
    """Тест с временным путем (встроенная фикстура pytest)"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, World!")
    assert test_file.read_text() == "Hello, World!"


# Захват stdout/stderr
def test_print_output(capsys):
    """Тест захвата вывода"""
    print("Hello from test")
    captured = capsys.readouterr()
    assert "Hello from test" in captured.out


# Конфигурация pytest в conftest.py (создать отдельно)
"""
# conftest.py - файл конфигурации pytest

import pytest

@pytest.fixture(scope="session")
def database():
    '''Фикстура уровня сессии для базы данных'''
    # Настройка БД для всех тестов
    db = "test_database_connection"
    yield db
    # Очистка после всех тестов
    print("Closing database")

@pytest.fixture(autouse=True)
def setup_and_teardown():
    '''Автоматически выполняется для каждого теста'''
    print("Setup before test")
    yield
    print("Teardown after test")

# Кастомные маркеры
pytest_plugins = []

def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow")
    config.addinivalue_line("markers", "integration: mark test as integration")
    config.addinivalue_line("markers", "unit: mark test as unit test")
"""

# Запуск pytest из командной строки:
"""
# Основные команды pytest:

pytest                          # Запуск всех тестов
pytest test_file.py            # Запуск тестов из конкретного файла
pytest -v                      # Verbose режим (подробный вывод)
pytest -s                      # Показать print выводы
pytest -x                      # Остановиться на первой ошибке
pytest --maxfail=3            # Остановиться после 3 ошибок
pytest -k "test_add"          # Запуск тестов содержащих "test_add" в имени
pytest -m slow                # Запуск тестов с маркером "slow"
pytest --tb=short             # Короткий traceback
pytest --tb=no                # Без traceback
pytest --collect-only         # Показать какие тесты будут запущены
pytest --durations=10         # Показать 10 самых медленных тестов
pytest --cov=module_name      # Coverage отчет (нужен pytest-cov)
pytest --html=report.html     # HTML отчет (нужен pytest-html)

# Запуск конкретных тестов:
pytest test_file.py::test_function
pytest test_file.py::TestClass::test_method
"""

# Сравнение unittest vs pytest:
"""
UNITTEST vs PYTEST:

Unittest (встроенный в Python):
+ Входит в стандартную библиотеку
+ Следует xUnit паттерну
+ Хорошая интеграция с IDE
- Более verbose синтаксис
- Нужно наследоваться от TestCase
- Меньше встроенных возможностей

Pytest (внешняя библиотека):
+ Простой синтаксис (просто assert)
+ Мощные фикстуры
+ Параметризация из коробки
+ Богатая экосистема плагинов
+ Автообнаружение тестов
+ Лучший вывод при ошибках
- Нужно устанавливать отдельно
- Может быть избыточным для простых проектов

Рекомендация: для новых проектов лучше использовать pytest,
для поддержки старых или простых случаев - unittest.
"""