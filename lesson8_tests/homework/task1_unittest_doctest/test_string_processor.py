# Завдання 1. Модульне тестування з використанням unittest
#
# Напишіть простий застосунок для обробки рядків та напишіть модульні тести з використанням бібліотеки unittest.
# Створіть клас StringProcessor з методами:
#
# reverse_string(s: str) -> str: повертає перевернутий рядок.
# capitalize_string(s: str) -> str: робить першу літеру рядка великої.
# count_vowels(s: str) -> int: повертає кількість голосних у рядку.
# Напишіть тести для кожного методу, перевіряючи кілька різних сценаріїв:
#
# порожні рядки,
# рядки з різними регістрами,
# рядки з цифрами та символами.
# Використовуйте декоратор @unittest.skip для пропуску тесту,
# який тестує метод reverse_string з порожнім рядком, оскільки це відома проблема, яку ви плануєте вирішити пізніше.

import unittest

from lesson8_tests.homework.task1_unittest_doctest.string_processor import StringProcessor


class TestStringProcessor(unittest.TestCase):
    """
    Тестовий клас для перевірки функціональності StringProcessor.
    """

    def setUp(self):
        """Ініціалізація об'єкта StringProcessor перед кожним тестом."""
        self.processor = StringProcessor()

    # Тести для методу reverse_string
    def test_reverse_string_normal(self):
        """Тест реверсування звичайного рядка."""
        self.assertEqual(self.processor.reverse_string("hello"), "olleh")
        self.assertEqual(self.processor.reverse_string("Python"), "nohtyP")
        self.assertEqual(self.processor.reverse_string("12345"), "54321")

    @unittest.skip("Відома проблема з порожніми рядками, буде вирішена пізніше")
    def test_reverse_string_empty(self):
        """Тест реверсування порожнього рядка (пропущений)."""
        self.assertEqual(self.processor.reverse_string(""), "")

    def test_reverse_string_single_char(self):
        """Тест реверсування рядка з одним символом."""
        self.assertEqual(self.processor.reverse_string("a"), "a")
        self.assertEqual(self.processor.reverse_string("5"), "5")
        self.assertEqual(self.processor.reverse_string("!"), "!")

    def test_reverse_string_with_symbols(self):
        """Тест реверсування рядка з символами та цифрами."""
        self.assertEqual(self.processor.reverse_string("Hello123!"), "!321olleH")
        self.assertEqual(self.processor.reverse_string("@#$%"), "%$#@")

    def test_reverse_string_mixed_case(self):
        """Тест реверсування рядка з різними регістрами."""
        self.assertEqual(self.processor.reverse_string("HeLLo"), "oLLeH")
        self.assertEqual(self.processor.reverse_string("PyThOn"), "nOhTyP")

    # Тести для методу capitalize_string
    def test_capitalize_string_normal(self):
        """Тест капіталізації звичайного рядка."""
        self.assertEqual(self.processor.capitalize_string("hello"), "Hello")
        self.assertEqual(self.processor.capitalize_string("python"), "Python")
        self.assertEqual(self.processor.capitalize_string("world"), "World")

    def test_capitalize_string_empty(self):
        """Тест капіталізації порожнього рядка."""
        self.assertEqual(self.processor.capitalize_string(""), "")

    def test_capitalize_string_all_uppercase(self):
        """Тест капіталізації рядка в верхньому регістрі."""
        self.assertEqual(self.processor.capitalize_string("HELLO"), "Hello")
        self.assertEqual(self.processor.capitalize_string("PYTHON"), "Python")

    def test_capitalize_string_with_numbers(self):
        """Тест капіталізації рядка з цифрами."""
        self.assertEqual(self.processor.capitalize_string("hello123"), "Hello123")
        self.assertEqual(self.processor.capitalize_string("123hello"), "123hello")

    def test_capitalize_string_with_symbols(self):
        """Тест капіталізації рядка з символами."""
        self.assertEqual(self.processor.capitalize_string("!hello"), "!hello")
        self.assertEqual(self.processor.capitalize_string("hello!world"), "Hello!world")

    def test_capitalize_string_single_char(self):
        """Тест капіталізації рядка з одним символом."""
        self.assertEqual(self.processor.capitalize_string("a"), "A")
        self.assertEqual(self.processor.capitalize_string("Z"), "Z")

    # Тести для методу count_vowels
    def test_count_vowels_normal(self):
        """Тест підрахунку голосних у рядку."""
        self.assertEqual(self.processor.count_vowels("hello"), 2)  # e, o
        self.assertEqual(self.processor.count_vowels("programming"), 3)
        self.assertEqual(self.processor.count_vowels("aeiou"), 5)
        self.assertEqual(self.processor.count_vowels("hello привіт"), 4)  # e, o, и, і
        self.assertEqual(self.processor.count_vowels("Python програма"), 4)  # o, о, а, а

    def test_count_vowels_empty(self):
        """Тест підрахунку голосних у порожньому рядку."""
        self.assertEqual(self.processor.count_vowels(""), 0)

    def test_count_vowels_no_vowels(self):
        """Тест підрахунку голосних у рядку без голосних."""
        self.assertEqual(self.processor.count_vowels("bcdfg!@#$%12345"), 0)

    def test_count_vowels_mixed_case(self):
        """Тест підрахунку голосних у рядку з різними регістрами."""
        self.assertEqual(self.processor.count_vowels("AEIOU"), 5)
        self.assertEqual(self.processor.count_vowels("PyThOn"), 1)  # o
