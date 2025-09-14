# Створіть простий консольний калькулятор, який дозволяє виконувати основні арифметичні операції (+, -, *, /).
# Реалізуйте у ньому обробку таких винятків: ZeroDivisionError, ValueError
# Створіть власний виняток UnknownOperationError для невідомих операцій.
# 	Додаткове завдання: додайте можливість роботи з десятковими числами та обробку винятків, пов'язаних із переповненням.
from decimal import Decimal, Overflow, InvalidOperation, ROUND_HALF_UP
from typing import Optional


class UnknownOperationError(Exception):
    """Виняток для невідомих операцій."""

    def __init__(self, message: str = "Невідома операція! Використовуйте: +, -, *, /"):
        self.message = message
        super().__init__(self.message)


OPERATIONS = {'+', '-', '*', '/'}


def get_operand(prompt: str = "Введіть число: ") -> Decimal:
    """
    Отримує число від користувача.
    Returns:
        Decimal: число
    """
    while True:
        try:
            user_input = input(prompt).strip()
            # Проверка на пустой ввод ДО создания Decimal
            if not user_input:
                print("Введіть число!")
                continue
            operand = Decimal(user_input)
            return operand
        except InvalidOperation:
            print('Має бути число!')


def get_operation(prompt: str = "Введіть операцію(+, -, *, /): ") -> str:
    """Отримує операцію від користувача з валідацією."""
    while True:
        try:
            operation = input(prompt).strip()

            if not operation:
                print(prompt)
                continue

            if operation not in OPERATIONS:
                raise UnknownOperationError(
                    f"Операція '{operation}' невідома! "
                    f"Доступні: {', '.join(OPERATIONS)}"
                )

            return operation

        except UnknownOperationError as e:
            print(f" {e}")
        except Exception as e:
            print(f"Несподівана помилка: {e}")


def calculate(num1: Decimal, num2: Decimal, operation: str) -> Optional[Decimal]:
    """
    Виконує арифметичну операцію.

    Args:
    num1: Перше число
    num2: Друге число
    operation: Операція

    Returns:
    Optional[Decimal]: Результат або None при помилці
    """
    print(operation)
    if operation == '+':
        return num1 + num2
    try:
        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 == 0:
                raise ZeroDivisionError("Поділ на нуль неможливий!")
            result = num1 / num2
        else:
            raise UnknownOperationError(f"Операція '{operation}' не підтримується")

        # Проверка на переполнение
        if abs(result) > Decimal('1E+308'):  # Орієнтовний ліміт для великих чисел
            raise Overflow("Результат слишком велик!")

        return result

    except ZeroDivisionError as e:
        print(f"Помилка поділу: {e}")
        return None
    except Overflow as e:
        print(f"Переповнення: {e}")
        return None
    except InvalidOperation as e:
        print(f"Некоректна операція: {e}")
        return None
    except Exception as e:
        print(f"Несподівана помилка під час обчислення: {e}")
        return None


def format_number(number: Decimal, max_decimals: int = 5) -> str:
    """Форматує число для гарного відображення."""
    if number == 0:
        return "0"

    # Перевіряємо, чи є число цілим
    if number == number.to_integral_value():
        return str(int(number))

        # Округлити до max_decimals знаків після коми
    quantize_template = Decimal('0.' + '0' * max_decimals)
    rounded = number.quantize(quantize_template, rounding=ROUND_HALF_UP)

    # Забираємо зайві нулі
    return str(rounded.normalize())

# --------------------------------------------------------------
# Отримання даных
operand1 = get_operand("Перше число: ")
operand2 = get_operand("Друге число: ")
operation = get_operation()

# Розрахунки
result = calculate(operand1, operand2, operation)

# Вивод результату
expression = f"{format_number(operand1)} {operation} {format_number(operand2)}"
if result is not None:
    print(f"\nРезультат: {expression} = {format_number(result)}")
else:
    print(f"\nПомилка у виразі: {expression}")
