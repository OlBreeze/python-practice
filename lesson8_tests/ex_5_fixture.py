"""
Тести з використанням pytest та фікстури.
Фікстура setup_numbers готує початкові значення num1 та num2 для тестів.
"""

import pytest
from calculator import add  # функция add должна быть в файле calculator.py


@pytest.fixture
def setup_numbers():
    num1 = 5
    num2 = 10
    return num1, num2


def test_addition_with_fixture(setup_numbers):
    num1, num2 = setup_numbers
    assert add(num1, num2) == 15


def test_addition_with_negative_fixture(setup_numbers):
    num1, num2 = setup_numbers
    assert add(-num1, num2) == 5


def test_addition_with_zero(setup_numbers):
    num1, num2 = setup_numbers
    assert add(0, num2) == 10
    assert add(num1, 0) == 5


def test_addition_with_large_numbers():
    assert add(1000, 2000) == 3000

# !!!!!!!
@pytest.fixture
def file_handler(tmp_path):
    # создаём временный файл
    file = tmp_path / "file.py"
    file.write_text("Hello world")

    # отдаём файл тестам
    yield file

    # удаляем файл после теста
    file.unlink()


def test_file_content(file_handler):
    # читаем содержимое временного файла
    content = file_handler.read_text()
    assert content == "Hello world"

#     !!!!!!!!!!!!!!!!!!!!!
# несколько pytest.fixture связаны между собой:
# db_connection — имитирует подключение к БД (scope="module", т.е. выполняется один раз на модуль).
# user — возвращает словарь с данными пользователя.
# user_greeting — использует фикстуру user, чтобы сформировать приветствие.

@pytest.fixture(scope="module")
def db_connection():
    print("Connecting to database")
    return {"status": "connected"}

@pytest.fixture
def user():
    return {"name": "John", "age": 25}

@pytest.fixture
def user_greeting(user):
    return f'Hello {user["name"]}!'

def test_db_connection(db_connection):
    assert db_connection["status"] == "connected"

def test_user(user):
    assert user["name"] == "John"
    assert user["age"] == 25

def test_user_greeting(user_greeting):
    assert user_greeting == "Hello John!"


# !!!!
# пример с маркировкой тестов в pytest:
# @pytest.mark.smoke — быстрые «smoke» тесты (проверка базовой работоспособности).
# @pytest.mark.regression — регрессионные тесты (проверка, что старое работает).
# @pytest.mark.skip — пропуск теста с указанием причины.
"""
Використання маркування @pytest.mark.smoke та @pytest.mark.regression для позначення тестів за їх типом.
Маємо тест, який ми пропускаємо за допомогою @pytest.mark.skip, оскільки він ще не реалізований.
"""

@pytest.mark.smoke
def test_addition_smoke():
    assert add(2, 3) == 5

@pytest.mark.regression
def test_addition_regression():
    assert add(-2, 3) == 1

@pytest.mark.skip(reason="Not implemented yet")
def test_addition_pending():
    assert add(0, 0) == 0

