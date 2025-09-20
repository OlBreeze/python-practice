# Завдання 5. Тестування винятків у pytest (опціонально)
#
# Напишіть функцію divide(a: int, b: int) -> float, яка поділяє два числа.
# Якщо знаменник дорівнює нулю, функція повинна викидати виняток ZeroDivisionError.
# Напишіть тести з використанням pytest, які:
# перевіряють коректний поділ,
# перевіряють викидання виключення ZeroDivisionError, якщо знаменник дорівнює нулю.
# Додайте тест із параметризацією для перевірки поділу з різними значеннями.

# test_divide.py - тести
import pytest
from divide import divide


class TestDivide:
    """Клас для тестування функції divide"""

    def test_correct_division(self):
        """Тест коректного ділення"""
        assert divide(10, 2) == 5.0
        assert divide(15, 3) == 5.0
        assert divide(7, 2) == 3.5
        assert divide(-10, 2) == -5.0
        assert divide(10, -2) == -5.0
        assert divide(-10, -2) == 5.0

    def test_zero_division_error(self):
        """Тест викидання ZeroDivisionError при діленні на нуль"""
        with pytest.raises(ZeroDivisionError) as exc_info:
            divide(10, 0)

        # Перевіряємо повідомлення винятку
        assert str(exc_info.value) == "Ділення на нуль неможливе"

    def test_zero_division_error_negative_zero(self):
        """Тест викидання ZeroDivisionError при діленні на -0"""
        with pytest.raises(ZeroDivisionError):
            divide(5, 0)

    def test_zero_numerator(self):
        """Тест ділення нуля на число (має повертати 0)"""
        assert divide(0, 5) == 0.0
        assert divide(0, -3) == 0.0

    @pytest.mark.parametrize("a,b,expected", [
        (10, 2, 5.0),
        (15, 3, 5.0),
        (7, 2, 3.5),
        (-10, 2, -5.0),
        (10, -2, -5.0),
        (-10, -2, 5.0),
        (0, 5, 0.0),
        (1, 1, 1.0),
        (100, 4, 25.0),
        (9, 3, 3.0),
        (-15, -3, 5.0),
        (22, 7, 22 / 7),  # Перевірка з дробовим результатом
    ])
    def test_parametrized_division(self, a, b, expected):
        """Параметризований тест для різних значень ділення"""
        result = divide(a, b)
        assert result == pytest.approx(expected, rel=1e-9)

    @pytest.mark.parametrize("a,b", [
        (10, 0),
        (-5, 0),
        (0, 0),
        (100, 0),
        (-100, 0),
    ])
    def test_parametrized_zero_division(self, a, b):
        """Параметризований тест для перевірки ZeroDivisionError"""
        with pytest.raises(ZeroDivisionError):
            divide(a, b)

    def test_large_numbers(self):
        """Тест з великими числами"""
        assert divide(1000000, 1000) == 1000.0
        assert divide(999999999, 3) == 333333333.0

    def test_small_numbers(self):
        """Тест з малими числами"""
        assert divide(1, 10) == 0.1
        assert divide(1, 100) == 0.01


# Додатковий набір тестів з використанням fixtures
class TestDivideWithFixtures:
    """Тести з використанням fixtures"""

    @pytest.fixture
    def sample_data(self):
        """Фікстура з тестовими даними"""
        return [
            (10, 2, 5.0),
            (20, 4, 5.0),
            (-8, -2, 4.0),
            (15, -3, -5.0)
        ]

    def test_with_fixture_data(self, sample_data):
        """Тест з використанням fixture"""
        for a, b, expected in sample_data:
            assert divide(a, b) == expected

# Приклад запуску тестів:
# В терміналі виконайте:
# pip install pytest
# pytest test_divide.py -v
#
# Для запуску з покриттям коду:
# pip install pytest-cov
# pytest test_divide.py --cov=divide --cov-report=html
#
# Для запуску конкретного тесту:
# pytest test_divide.py::TestDivide::test_correct_division -v