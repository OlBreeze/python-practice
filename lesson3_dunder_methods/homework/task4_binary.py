# 4. Binary
# 1. Реалізуйте клас BinaryNumber, який представляє двійкове число.
#   Додайте методи для виконання двійкових операцій: AND (__and__), OR (__or__), XOR (__xor__) та NOT (__invert__).
# 2. Напишіть тест для цих операцій.

class BinaryNumber:
    def __init__(self, value: str) -> None:
        """Ініціалізує об'єкт BinaryNumber на основі рядка з двійковим числом."""
        if not all(c in '01' for c in value):
            raise ValueError("Binary number must contain only '0' and '1'")
        self.value: str = value.zfill(8)  # .zfill(n) дополняет строку слева нулями, чтобы её длина стала n символов. "101" → "00000101"

    def __repr__(self) -> str:
        """
        Повертає строкове представлення двійкового числа.
        :return: Рядок у форматі 'BinaryNumber(10101010)'
        """
        return f"BinaryNumber({self.value})"

    def __int__(self) -> int:
        """Перетворює двійкове число у десяткове."""
        return int(self.value, 2)  # приведение типов, int(...) может принимать строку и систему счисления.

    def __and__(self, other: 'BinaryNumber') -> 'BinaryNumber':
        """
        Бітова операція AND (&) між двома двійковими числами.
        :param other: Інший BinaryNumber
        :return: Результат операції AND як BinaryNumber
        """
        result = int(self) & int(other)  # выполняется битовая операция И (AND) между двумя целыми числами
        return BinaryNumber(bin(result)[2:]  # Преобразуем результат обратно в двоичную строку.bin(...) возвращает строку с префиксом '0b', который нужно убрать.
                            .zfill(len(self.value)))  # .zfill(len(self.value)) - Дополняем строку слева нулями до нужной длины — такой же, как у self.value

    def __or__(self, other: 'BinaryNumber') -> 'BinaryNumber':
        """
        Бітова операція OR (|) між двома двійковими числами.

        :param other: Інший BinaryNumber
        :return: Результат операції OR як BinaryNumber
        """
        result = int(self) | int(other)
        return BinaryNumber(bin(result)[2:].zfill(len(self.value)))

    def __xor__(self, other: 'BinaryNumber') -> 'BinaryNumber':
        """
        Бітова операція XOR (^) між двома двійковими числами.

        :param other: Інший BinaryNumber
        :return: Результат операції XOR як BinaryNumber
        """
        result = int(self) ^ int(other)
        return BinaryNumber(bin(result)[2:].zfill(len(self.value)))

    def __invert__(self) -> 'BinaryNumber':
        """
        Бітова операція NOT (~) — інверсія бітів.

        :return: Результат інверсії як BinaryNumber
        """
        inverted = ''.join('1' if bit == '0' else '0' for bit in self.value)
        return BinaryNumber(inverted)

# ========================
a = BinaryNumber("10101010")
b = BinaryNumber("11001100")

print("a:       ", a)
print("b:       ", b)
print("a & b:   ", a & b)
print("a | b:   ", a | b)
print("a ^ b:   ", a ^ b)
print("~a:      ", ~a) #побитовая инверсия, или NOT (логическое отрицание по битам).это не то же самое, что not a в логике
print("~b:      ", ~b)  # Оператор ~ инвертирует каждый бит числа: 0 становится 1, 1 становится 0

