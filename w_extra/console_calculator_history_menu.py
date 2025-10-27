"""
Оптимизированный консольный калькулятор с обработкой исключений.

Поддерживает:
- Основные арифметические операции (+, -, *, /)
- Работу с десятичными числами (Decimal для точности)
- Обработку всех типов ошибок
- Пользовательские исключения
- Циклическую работу
"""

from decimal import Decimal, InvalidOperation, Overflow
from typing import Union, Tuple, Optional


class UnknownOperationError(Exception):
    """Исключение для неизвестных операций."""

    def __init__(self, message: str = "Неизвестная операция! Используйте: +, -, *, /"):
        self.message = message
        super().__init__(self.message)


class Calculator:
    """Консольный калькулятор с обработкой исключений."""

    OPERATIONS = {'+', '-', '*', '/'}

    def __init__(self):
        """Инициализация калькулятора."""
        self.history = []

    def get_number(self, prompt: str = "Введите число: ") -> Decimal:
        """
        Получает число от пользователя с валидацией.

        Args:
            prompt: Текст приглашения для ввода

        Returns:
            Decimal: Введенное число
        """
        while True:
            try:
                user_input = input(prompt).strip()

                # Проверка на пустой ввод
                if not user_input:
                    print("❌ Введите число!")
                    continue

                # Преобразование в Decimal для точности
                number = Decimal(user_input)
                return number

            except InvalidOperation:
                print("❌ Некорректное число! Попробуйте еще раз.")
            except KeyboardInterrupt:
                print("\n👋 Выход из программы.")
                raise
            except Exception as e:
                print(f"❌ Неожиданная ошибка: {e}")

    def get_operation(self) -> str:
        """
        Получает операцию от пользователя с валидацией.

        Returns:
            str: Валидная операция
        """
        while True:
            try:
                operation = input("Введите операцию (+, -, *, /): ").strip()

                if not operation:
                    print("❌ Введите операцию!")
                    continue

                if operation not in self.OPERATIONS:
                    raise UnknownOperationError(
                        f"Операция '{operation}' неизвестна! "
                        f"Доступные: {', '.join(sorted(self.OPERATIONS))}"
                    )

                return operation

            except UnknownOperationError as e:
                print(f"❌ {e}")
            except KeyboardInterrupt:
                print("\n👋 Выход из программы.")
                raise
            except Exception as e:
                print(f"❌ Неожиданная ошибка: {e}")

    def calculate(self, num1: Decimal, num2: Decimal, operation: str) -> Optional[Decimal]:
        """
        Выполняет арифметическую операцию.

        Args:
            num1: Первое число
            num2: Второе число
            operation: Операция

        Returns:
            Optional[Decimal]: Результат или None при ошибке
        """
        try:
            if operation == '+':
                result = num1 + num2
            elif operation == '-':
                result = num1 - num2
            elif operation == '*':
                result = num1 * num2
            elif operation == '/':
                if num2 == 0:
                    raise ZeroDivisionError("Деление на ноль невозможно!")
                result = num1 / num2
            else:
                # Это не должно произойти из-за валидации, но для безопасности
                raise UnknownOperationError(f"Операция '{operation}' не поддерживается")

            # Проверка на переполнение
            if abs(result) > Decimal('1E+308'):  # Примерный лимит для больших чисел
                raise Overflow("Результат слишком велик!")

            return result

        except ZeroDivisionError as e:
            print(f"❌ Ошибка деления: {e}")
            return None
        except Overflow as e:
            print(f"❌ Переполнение: {e}")
            return None
        except InvalidOperation as e:
            print(f"❌ Некорректная операция: {e}")
            return None
        except Exception as e:
            print(f"❌ Неожиданная ошибка при вычислении: {e}")
            return None

    def format_number(self, number: Decimal) -> str:
        """
        Форматирует число для красивого отображения.

        Args:
            number: Число для форматирования

        Returns:
            str: Отформатированное число
        """
        # Убираем лишние нули после запятой
        if number == number.to_integral_value():
            return str(int(number))
        else:
            return str(number.normalize())

    def add_to_history(self, num1: Decimal, operation: str, num2: Decimal, result: Optional[Decimal]) -> None:
        """
        Добавляет операцию в историю.

        Args:
            num1: Первое число
            operation: Операция
            num2: Второе число
            result: Результат
        """
        if result is not None:
            self.history.append({
                'expression': f"{self.format_number(num1)} {operation} {self.format_number(num2)}",
                'result': self.format_number(result)
            })
        else:
            self.history.append({
                'expression': f"{self.format_number(num1)} {operation} {self.format_number(num2)}",
                'result': 'Ошибка'
            })

    def show_history(self) -> None:
        """Показывает историю вычислений."""
        if not self.history:
            print("📊 История пуста.")
            return

        print("\n📊 История вычислений:")
        print("-" * 30)
        for i, calc in enumerate(self.history[-10:], 1):  # Показываем последние 10
            print(f"{i}. {calc['expression']} = {calc['result']}")
        print("-" * 30)

    def show_menu(self) -> str:
        """
        Показывает меню и возвращает выбор пользователя.

        Returns:
            str: Выбор пользователя
        """
        print("\n🧮 КАЛЬКУЛЯТОР")
        print("1. Выполнить вычисление")
        print("2. Показать историю")
        print("3. Очистить историю")
        print("4. Выход")

        while True:
            try:
                choice = input("\nВыберите пункт (1-4): ").strip()
                if choice in ['1', '2', '3', '4']:
                    return choice
                print("❌ Выберите пункт от 1 до 4!")
            except KeyboardInterrupt:
                print("\n👋 Выход из программы.")
                return '4'
            except Exception as e:
                print(f"❌ Ошибка: {e}")

    def run_single_calculation(self) -> None:
        """Выполняет одно вычисление."""
        try:
            print("\n➕ НОВОЕ ВЫЧИСЛЕНИЕ")
            print("-" * 20)

            # Получение данных
            num1 = self.get_number("Первое число: ")
            operation = self.get_operation()
            num2 = self.get_number("Второе число: ")

            # Вычисление
            result = self.calculate(num1, operation, num2)

            # Вывод результата
            expression = f"{self.format_number(num1)} {operation} {self.format_number(num2)}"
            if result is not None:
                print(f"\n✅ Результат: {expression} = {self.format_number(result)}")
            else:
                print(f"\n❌ Ошибка в выражении: {expression}")

            # Добавление в историю
            self.add_to_history(num1, operation, num2, result)

        except KeyboardInterrupt:
            print("\n⏸️ Вычисление прервано.")
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")

    def run(self) -> None:
        """Основной цикл программы."""
        print("🎉 Добро пожаловать в калькулятор!")
        print("Поддерживает целые и десятичные числа.")

        try:
            while True:
                choice = self.show_menu()

                if choice == '1':
                    self.run_single_calculation()

                elif choice == '2':
                    self.show_history()

                elif choice == '3':
                    self.history.clear()
                    print("✅ История очищена!")

                elif choice == '4':
                    print("👋 Спасибо за использование калькулятора!")
                    break

        except KeyboardInterrupt:
            print("\n👋 Программа завершена пользователем.")
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")


def main():
    """Точка входа в программу."""
    calculator = Calculator()
    calculator.run()


if __name__ == "__main__":
    main()


# ========================================
# ДЕМОНСТРАЦИЯ И ТЕСТЫ
# ========================================

def demo():
    """Демонстрация возможностей калькулятора."""
    print("🎯 ДЕМОНСТРАЦИЯ КАЛЬКУЛЯТОРА")
    print("=" * 40)

    calc = Calculator()

    # Тестовые случаи
    test_cases = [
        (Decimal('10'), '+', Decimal('5'), "Обычное сложение"),
        (Decimal('10.5'), '-', Decimal('3.2'), "Десятичные числа"),
        (Decimal('4'), '*', Decimal('7'), "Умножение"),
        (Decimal('15'), '/', Decimal('3'), "Деление"),
        (Decimal('10'), '/', Decimal('0'), "Деление на ноль"),
        (Decimal('1E+200'), '*', Decimal('1E+200'), "Переполнение"),
    ]

    for num1, op, num2, description in test_cases:
        print(f"\n📝 Тест: {description}")
        print(f"   Выражение: {calc.format_number(num1)} {op} {calc.format_number(num2)}")

        result = calc.calculate(num1, num2, op)
        if result is not None:
            print(f"   Результат: {calc.format_number(result)}")
        else:
            print("   Результат: Ошибка")

        calc.add_to_history(num1, op, num2, result)

    # Показать историю
    calc.show_history()

# Раскомментируйте для демонстрации
demo()