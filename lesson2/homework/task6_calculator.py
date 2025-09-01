# Завдання 6: Калькулятор з використанням замикань
# arr_symbols = ['+', '-', '*', '/', '%']
from numbers import Number
from typing import Callable, Union


def create_operator(operator: str) -> Callable[[Number, Number], Union[Number, str]]:
    """
    Створює математичну операцію на основі переданого оператора.

    Args:
        operator (str): Символ операції ('+', '-', '*', '/').

    Returns:
        Callable[[Number, Number], Union[Number, str]]:
            Функція, яка приймає два числа і виконує операцію.
            У разі помилки (наприклад, ділення на нуль) повертає повідомлення з помилкою.
    """

    def operation(a: Number, b: Number) -> Union[Number, str]:
        """
        Виконує математичну операцію між двома числами.

        Args:
            a (Number): Перше число.
            b (Number): Друге число.

        Returns:
            Union[Number, str]: Результат обчислення або повідомлення про помилку.
        """
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            if b == 0:
                return "Помилка: Ділення на нуль!"
            return a / b
        else:
            return "Невідомий оператор"

    return operation


# print(create_operator('+')(10, 5)) # можна й так

add = create_operator('+')
subtract = create_operator('-')
multiply = create_operator('*')
divide = create_operator('/')

# Check
print(f"Додавання: 10 + 5 = {add(10, 5)}")
print(f"Додавання: 15 + 5 = {add(15, 5)}")
print(f"Додавання: 55 + 5 = {add(55, 5)}")

print(f"\nВіднімання: 10 - 5 = {subtract(10, 5)}")
print(f"Множення: 10 * 5 = {multiply(10, 5)}")
print(f"Ділення: 10 / 5 = {divide(10, 5)}")
print(f"Ділення на нуль: 10 / 0 = {divide(10, 0)}")
