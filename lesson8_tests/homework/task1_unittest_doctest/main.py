import unittest

from lesson8_tests.homework.task1_unittest.string_processor import StringProcessor
from lesson8_tests.homework.task1_unittest.test_string_processor import TestStringProcessor


def run_tests():
    """
    Запускає всі тести з детальним виводом результатів.
    """
    # Створення test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestStringProcessor)

    # Запуск тестів
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Виведення підсумкової статистики
    print(f"Всього тестів: {result.testsRun}")
    print(f"Помилки: {len(result.errors)}")
    print(f"Невдалі тести: {len(result.failures)}")
    print(f"Пропущені тести: {len(result.skipped)}")

    if result.wasSuccessful():
        print("✅ Всі тести пройдені успішно!\n")
    else:
        print("❌ Деякі тести не пройдені.\n")

    return result


if __name__ == "__main__":
    # Демонстрація роботи StringProcessor
    processor = StringProcessor()

    test_string = "Hello World 123!"
    print(f"Оригінальний рядок: '{test_string}'")
    print(f"Перевернутий: '{processor.reverse_string(test_string)}'")
    print(f"Капіталізований: '{processor.capitalize_string(test_string.lower())}'")
    print(f"Кількість голосних: {processor.count_vowels(test_string)}")

    print("\nЗапуск модульних тестів:")
    print("-" * 50)

    # Запуск тестів
    run_tests()