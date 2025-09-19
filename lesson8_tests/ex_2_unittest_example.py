# test_example.py1 - тесты
import unittest
from example_1 import add, factorial, divide, is_even, get_user_info, get_numbers


class TestMathFunctions(unittest.TestCase):

    # Базовые assert методы
    def test_add_positive_numbers(self):
        """Тест сложения положительных чисел"""
        result = add(2, 3)
        self.assertEqual(result, 5)  # Проверка равенства

    def test_add_negative_numbers(self):
        """Тест сложения отрицательных чисел"""
        result = add(-2, -3)
        self.assertEqual(result, -5)

    def test_add_zero(self):
        """Тест сложения с нулем"""
        result = add(5, 0)
        self.assertEqual(result, 5)

    # Тесты с assertTrue/False
    def test_is_even(self):
        """Тест проверки четности"""
        self.assertTrue(is_even(4))  # 4 четное
        self.assertFalse(is_even(3))  # 3 нечетное
        self.assertTrue(is_even(0))  # 0 четное

    # Тест факториала с различными assert
    def test_factorial_zero(self):
        """Тест факториала нуля"""
        result = factorial(0)
        self.assertEqual(result, 1)

    def test_factorial_positive(self):
        """Тест факториала положительного числа"""
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(3), 6)

    # Тест исключений
    def test_factorial_negative(self):
        """Тест факториала отрицательного числа"""
        with self.assertRaises(ValueError):
            factorial(-1)

        # Можно также проверить сообщение исключения
        with self.assertRaises(ValueError) as context:
            factorial(-5)
        self.assertEqual(str(context.exception), 'n must be positive')

    def test_divide_by_zero(self):
        """Тест деления на ноль"""
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

    # Тесты с приблизительным равенством
    def test_divide_float_result(self):
        """Тест деления с плавающей точкой"""
        result = divide(10, 3)
        self.assertAlmostEqual(result, 3.333333, places=5)  # Точность до 5 знаков

    # Тесты с None
    def test_none_values(self):
        """Тест работы с None"""
        value = None
        self.assertIsNone(value)

        not_none_value = "something"
        self.assertIsNotNone(not_none_value)

    # Тесты с коллекциями
    def test_list_contents(self):
        """Тест содержимого списков"""
        numbers = get_numbers()

        # Проверка содержимого списка
        self.assertIn(3, numbers)  # 3 есть в списке
        self.assertNotIn(10, numbers)  # 10 нет в списке

        # Проверка длины
        self.assertEqual(len(numbers), 5)

        # Проверка типа
        self.assertIsInstance(numbers, list)

    def test_dictionary_contents(self):
        """Тест содержимого словарей"""
        user_info = get_user_info()

        # Проверка ключей
        self.assertIn('name', user_info)
        self.assertIn('age', user_info)

        # Проверка значений
        self.assertEqual(user_info['name'], 'John')
        self.assertEqual(user_info['age'], 25)

        # Проверка типа
        self.assertIsInstance(user_info, dict)

    # Тесты сравнения
    def test_comparisons(self):
        """Тест операций сравнения"""
        a, b = 10, 5

        self.assertGreater(a, b)  # a > b
        self.assertGreaterEqual(a, 10)  # a >= 10
        self.assertLess(b, a)  # b < a
        self.assertLessEqual(b, 5)  # b <= 5

    # Тест с кастомным сообщением об ошибке
    def test_with_custom_message(self):
        """Тест с кастомным сообщением"""
        result = add(2, 2)
        self.assertEqual(result, 4, "Сложение 2 + 2 должно быть равно 4")

    # setUp и tearDown методы
    def setUp(self):
        """Выполняется перед каждым тестом"""
        self.test_data = [1, 2, 3, 4, 5]
        print("Настройка для теста...")

    def tearDown(self):
        """Выполняется после каждого теста"""
        print("Очистка после теста...")

    def test_using_setup_data(self):
        """Тест использующий данные из setUp"""
        self.assertEqual(len(self.test_data), 5)
        self.assertIn(3, self.test_data)


class TestStringMethods(unittest.TestCase):
    """Отдельный класс для тестирования строковых методов"""

    def test_string_methods(self):
        """Тест строковых методов"""
        text = "Hello World"

        # Проверка регистра
        self.assertTrue(text.isupper() == False)
        self.assertTrue(text.islower() == False)

        # Проверка начала/конца строки
        self.assertTrue(text.startswith('Hello'))
        self.assertTrue(text.endswith('World'))

        # Проверка содержимого
        self.assertIn('World', text)

        # Проверка регулярных выражений
        import re
        self.assertRegex(text, r'Hello.*World')


# Дополнительные assert методы с примерами
class TestAdvancedAssertions(unittest.TestCase):
    """Продвинутые примеры assert методов"""

    def test_sequence_equal(self):
        """Тест сравнения последовательностей"""
        list1 = [1, 2, 3]
        list2 = [1, 2, 3]
        tuple1 = (1, 2, 3)

        self.assertEqual(list1, list2)
        self.assertListEqual(list1, list2)  # Специально для списков
        self.assertTupleEqual(tuple1, (1, 2, 3))  # Специально для кортежей

    def test_dict_equal(self):
        """Тест сравнения словарей"""
        dict1 = {'a': 1, 'b': 2}
        dict2 = {'a': 1, 'b': 2}

        self.assertDictEqual(dict1, dict2)

    def test_set_equal(self):
        """Тест сравнения множеств"""
        set1 = {1, 2, 3}
        set2 = {3, 2, 1}  # Порядок не важен

        self.assertSetEqual(set1, set2)

    def test_multiline_equal(self):
        """Тест многострочного текста"""
        text1 = """Первая строка
Вторая строка
Третья строка"""

        text2 = """Первая строка
Вторая строка
Третья строка"""

        self.assertMultiLineEqual(text1, text2)


# Пример использования подтестов
class TestSubTests(unittest.TestCase):
    """Примеры подтестов"""

    def test_factorial_multiple_values(self):
        """Тест факториала для нескольких значений"""
        test_cases = [
            (0, 1),
            (1, 1),
            (2, 2),
            (3, 6),
            (4, 24),
            (5, 120)
        ]

        for n, expected in test_cases:
            with self.subTest(n=n):
                result = factorial(n)
                self.assertEqual(result, expected)


# Пример тестирования с моками (требует установки: pip install mock)
class TestWithMocks(unittest.TestCase):
    """Примеры использования mock объектов"""

    def test_with_patch(self):
        """Пример использования patch декоратора"""
        from unittest.mock import patch, MagicMock

        # Пример функции, которая использует внешний API
        def get_weather():
            import requests
            response = requests.get('http://api.weather.com')
            return response.json()

        # Мокируем requests.get
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {'temp': 20, 'condition': 'sunny'}
            mock_get.return_value = mock_response

            # result = get_weather()
            # self.assertEqual(result['temp'], 20)


# Пример параметризованных тестов (альтернатива подтестам)
class TestParametrized(unittest.TestCase):
    """Параметризованные тесты"""

    def _test_add_cases(self):
        """Вспомогательный метод с тест-кейсами"""
        return [
            (1, 2, 3),
            (0, 0, 0),
            (-1, 1, 0),
            (10, -5, 5),
            (2.5, 1.5, 4.0)
        ]

    def test_add_parametrized(self):
        """Параметризованный тест сложения"""
        for a, b, expected in self._test_add_cases():
            with self.subTest(a=a, b=b, expected=expected):
                result = add(a, b)
                self.assertEqual(result, expected)


# Полный справочник assert методов в unittest
"""
СПРАВОЧНИК ASSERT МЕТОДОВ:

Основные:
- assertEqual(a, b)           # a == b
- assertNotEqual(a, b)        # a != b
- assertTrue(x)               # bool(x) is True
- assertFalse(x)              # bool(x) is False
- assertIs(a, b)              # a is b
- assertIsNot(a, b)           # a is not b
- assertIsNone(x)             # x is None
- assertIsNotNone(x)          # x is not None
- assertIn(a, b)              # a in b
- assertNotIn(a, b)           # a not in b
- assertIsInstance(a, b)      # isinstance(a, b)
- assertNotIsInstance(a, b)   # not isinstance(a, b)

Числовые:
- assertAlmostEqual(a, b)     # round(a-b, 7) == 0
- assertNotAlmostEqual(a, b)  # round(a-b, 7) != 0
- assertGreater(a, b)         # a > b
- assertGreaterEqual(a, b)    # a >= b
- assertLess(a, b)            # a < b
- assertLessEqual(a, b)       # a <= b

Исключения:
- assertRaises(exc, fun, *args, **kwds)  # fun(*args, **kwds) вызывает exc
- assertRaisesRegex(exc, r, fun, *args, **kwds)  # + проверка regex

Строки:
- assertRegex(s, r)           # r.search(s)
- assertNotRegex(s, r)        # not r.search(s)

Коллекции:
- assertListEqual(a, b)       # Сравнение списков
- assertTupleEqual(a, b)      # Сравнение кортежей
- assertSetEqual(a, b)        # Сравнение множеств
- assertDictEqual(a, b)       # Сравнение словарей
- assertSequenceEqual(a, b)   # Сравнение последовательностей
- assertCountEqual(a, b)      # Сравнение без учета порядка
- assertMultiLineEqual(a, b)  # Сравнение многострочного текста

Предупреждения:
- assertWarns(warn, fun, *args, **kwds)       # Проверка предупреждений
- assertWarnsRegex(warn, r, fun, *args, **kwds)  # + проверка regex
"""

if __name__ == '__main__':
    # Запуск всех тестов
    unittest.main(verbosity=2)

    # Альтернативные способы запуска:

    # 1. Запуск конкретного класса тестов
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestMathFunctions)
    # unittest.TextTestRunner(verbosity=2).run(suite)

    # 2. Запуск конкретного теста
    # suite = unittest.TestSuite()
    # suite.addTest(TestMathFunctions('test_add_positive_numbers'))
    # unittest.TextTestRunner().run(suite)

    # 3. Запуск из командной строки:
    # python -m unittest ex_2_unittest_example.py
    # python -m unittest ex_2_unittest_example.TestMathFunctions
    # python -m unittest ex_2_unittest_example.TestMathFunctions.test_add_positive_numbers
    # python -m unittest discover -s tests -p "test_*.py"