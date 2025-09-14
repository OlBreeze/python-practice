"""
Различные способы округления чисел Decimal в Python
================================================
"""

from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN, getcontext
import math


def demo_rounding():
    """Демонстрация различных способов округления"""

    # Исходный результат
    result = Decimal('44.22') / Decimal('8454.325')
    print(f"Исходный результат: {result}")
    print("=" * 60)

    # ========================================
    # СПОСОБ 1: Округление до N знаков после запятой
    # ========================================
    print("1️⃣  ОКРУГЛЕНИЕ ДО N ЗНАКОВ ПОСЛЕ ЗАПЯТОЙ:")

    def format_decimal_places(number: Decimal, decimal_places: int = 5) -> str:
        """Округляет до определенного количества знаков после запятой"""
        # Создаем шаблон для округления (например, '0.00001' для 5 знаков)
        quantize_template = Decimal('0.' + '0' * decimal_places)
        rounded = number.quantize(quantize_template, rounding=ROUND_HALF_UP)
        return str(rounded.normalize())  # normalize() убирает лишние нули

    for places in [2, 3, 5, 8]:
        rounded = format_decimal_places(result, places)
        print(f"   До {places} знаков: {rounded}")

    # ========================================
    # СПОСОБ 2: Ограничение общего количества значащих цифр
    # ========================================
    print(f"\n2️⃣  ОГРАНИЧЕНИЕ ОБЩЕГО КОЛИЧЕСТВА ЗНАЧАЩИХ ЦИФР:")

    def format_significant_digits(number: Decimal, total_digits: int = 5) -> str:
        """Округляет до определенного количества значащих цифр"""
        if number == 0:
            return "0"

        # Устанавливаем точность контекста
        original_prec = getcontext().prec
        getcontext().prec = total_digits

        # Выполняем операцию с новой точностью
        rounded = +number  # Унарный плюс применяет текущую точность

        # Восстанавливаем исходную точность
        getcontext().prec = original_prec

        return str(rounded.normalize())

    for digits in [3, 5, 7, 10]:
        rounded = format_significant_digits(result, digits)
        print(f"   До {digits} значащих цифр: {rounded}")

    # ========================================
    # СПОСОБ 3: Гибридный подход (рекомендуемый)
    # ========================================
    print(f"\n3️⃣  ГИБРИДНЫЙ ПОДХОД (РЕКОМЕНДУЕМЫЙ):")

    def format_smart_rounding(number: Decimal, max_decimals: int = 5) -> str:
        """
        Умное округление:
        - Для больших чисел: ограничивает знаки после запятой
        - For малых чисел: сохраняет значащие цифры
        """
        abs_number = abs(number)

        if abs_number >= 1:
            # Для чисел >= 1: ограничиваем знаки после запятой
            quantize_template = Decimal('0.' + '0' * max_decimals)
            rounded = number.quantize(quantize_template, rounding=ROUND_HALF_UP)
        elif abs_number >= Decimal('0.001'):
            # Для чисел 0.001-0.999: до max_decimals знаков
            quantize_template = Decimal('0.' + '0' * max_decimals)
            rounded = number.quantize(quantize_template, rounding=ROUND_HALF_UP)
        else:
            # Для очень малых чисел: научная запись или значащие цифры
            original_prec = getcontext().prec
            getcontext().prec = max_decimals
            rounded = +number
            getcontext().prec = original_prec

        return str(rounded.normalize())

    test_numbers = [
        Decimal('44.22') / Decimal('8454.325'),  # Наш случай
        Decimal('123.456789'),
        Decimal('0.123456789'),
        Decimal('0.000123456789'),
        Decimal('0.000000123456789')
    ]

    for num in test_numbers:
        smart_rounded = format_smart_rounding(num, 5)
        print(f"   {num} → {smart_rounded}")

    # ========================================
    # СПОСОБ 4: Использование format() и f-strings
    # ========================================
    print(f"\n4️⃣  ИСПОЛЬЗОВАНИЕ format() И f-strings:")

    # С помощью format()
    formatted_1 = "{:.5f}".format(float(result))
    print(f"   format(.5f): {formatted_1}")

    # С помощью f-string
    float_result = float(result)
    formatted_2 = f"{float_result:.5f}"
    print(f"   f-string:.5f: {formatted_2}")

    # С помощью g для автоматического выбора
    formatted_3 = f"{float_result:.5g}"
    print(f"   f-string:.5g: {formatted_3}")

    # ========================================
    # РЕКОМЕНДУЕМОЕ РЕШЕНИЕ ДЛЯ КАЛЬКУЛЯТОРА
    # ========================================
    print(f"\n🎯 РЕКОМЕНДУЕМОЕ РЕШЕНИЕ ДЛЯ КАЛЬКУЛЯТОРА:")

    def format_calculator_result(number: Decimal, max_decimals: int = 5) -> str:
        """
        Оптимальное форматирование для калькулятора:
        - Убирает лишние нули
        - Ограничивает знаки после запятой
        - Обрабатывает особые случаи
        """
        if number == 0:
            return "0"

        # Округляем до max_decimals знаков после запятой
        quantize_template = Decimal('0.' + '0' * max_decimals)
        rounded = number.quantize(quantize_template, rounding=ROUND_HALF_UP)

        # Убираем лишние нули и форматируем
        normalized = rounded.normalize()
        result_str = str(normalized)

        # Если результат очень длинный, используем научную запись
        if len(result_str.replace('.', '').replace('-', '')) > 15:
            return f"{float(normalized):.5e}"

        return result_str

    # Тестирование рекомендуемого решения
    test_cases = [
        (Decimal('44.22') / Decimal('8454.325'), "Наш пример"),
        (Decimal('10') / Decimal('3'), "10/3"),
        (Decimal('1') / Decimal('7'), "1/7"),
        (Decimal('123.456789'), "Большое число"),
        (Decimal('0.000000123456789'), "Очень малое число"),
        (Decimal('10.0'), "Целое число"),
        (Decimal('0'), "Ноль")
    ]

    for num, description in test_cases:
        formatted = format_calculator_result(num, 5)
        print(f"   {description}: {formatted}")


# ========================================
# ОБНОВЛЕННЫЙ МЕТОД ДЛЯ КЛАССА CALCULATOR
# ========================================

def updated_format_number(number: Decimal, max_decimals: int = 5) -> str:
    """
    Обновленный метод format_number для класса Calculator.

    Args:
        number: Число для форматирования
        max_decimals: Максимальное количество знаков после запятой

    Returns:
        str: Отформатированное число
    """
    if number == 0:
        return "0"

    # Проверяем, является ли число целым
    if number == number.to_integral_value():
        return str(int(number))

    # Округляем до max_decimals знаков после запятой
    quantize_template = Decimal('0.' + '0' * max_decimals)
    rounded = number.quantize(quantize_template, rounding=ROUND_HALF_UP)

    # Убираем лишние нули
    result_str = str(rounded.normalize())

    # Если результат слишком длинный, используем научную запись
    if len(result_str.replace('.', '').replace('-', '')) > 12:
        return f"{float(rounded):.{max_decimals}e}"

    return result_str


if __name__ == "__main__":
    demo_rounding()

    print(f"\n" + "=" * 60)
    print("ПРИМЕР ИНТЕГРАЦИИ В КЛАСС Calculator:")
    print("=" * 60)

    # Демонстрация использования в классе Calculator
    result = Decimal('44.22') / Decimal('8454.325')

    print(f"Исходный результат: {result}")
    print(f"Старый format_number: {str(result.normalize())}")
    print(f"Новый format_number: {updated_format_number(result, 5)}")

    print(f"\nДругие примеры:")
    examples = [
        Decimal('10.000'),
        Decimal('3.141592653589793'),
        Decimal('0.000123456789'),
        Decimal('123456.789123456')
    ]

    for ex in examples:
        old = str(ex.normalize())
        new = updated_format_number(ex, 5)
        print(f"   {old} → {new}")