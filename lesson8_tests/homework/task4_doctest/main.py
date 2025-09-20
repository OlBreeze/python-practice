from lesson8_tests.homework.task4_doctest.task4_doctest import factorial, is_even


def main():
    """
    Демонстраційна функція для показу роботи функцій.
    """
    print("---- Тестування функції is_even ----")
    test_numbers = [0, 1, 2, 3, 4, 5, -2, -3, 100, 101]

    for num in test_numbers:
        result = is_even(num)
        print(f"is_even({num}) = {result}")

    print("\n---- Тестування функції factorial ----")
    factorial_numbers = [0, 1, 2, 3, 4, 5, 6]

    for num in factorial_numbers:
        result = factorial(num)
        print(f"factorial({num}) = {result}")

    print("\n--- Тестування factorial з від'ємним числом ---")
    try:
        factorial(-1)
    except ValueError as e:
        print(f"Помилка: {e}")


if __name__ == "__main__":
    import doctest

    print("Запуск doctest тестів...")
    print("-" * 50)

    # Запуск doctest з детальним виводом
    doctest.testmod(verbose=True)

    print("Демонстрація роботи функцій:")
    print("-" * 50)
    main()
