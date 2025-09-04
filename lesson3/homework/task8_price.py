# 8. Price class discussion before the PaymentGateway implementation
# 1.	Реалізуйте клас Price, що представляє ціну товару з можливістю заокруглення до двох десяткових знаків.
#       Додайте методи для додавання, віднімання та порівняння цін.
# 2.	Поміркуйте, як клас Price може бути використаний в майбутньому класі PaymentGateway для обробки фінансових транзакцій.

from decimal import Decimal, ROUND_HALF_UP
from typing import Union


class Price:
    """
    Клас для представлення ціни товару з точністю до 2 знаків після коми.
    """

    def __init__(self, amount: Union[float, str, Decimal]) -> None:
        """
        Ініціалізує об'єкт Price з заокругленням до 2 знаків після коми.

        :param amount: Значення ціни (float, str або Decimal)
        """
        self.amount: Decimal = self._round_to_two(Decimal(str(amount)))

    @staticmethod
    def _round_to_two(value: Decimal) -> Decimal:
        """
        Заокруглює значення до двох знаків після коми.

        :param value: Decimal
        :return: Decimal округлений
        """
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def __add__(self, other: "Price") -> "Price":
        """Додає дві ціни."""
        return Price(self.amount + other.amount)

    def __sub__(self, other: "Price") -> "Price":
        """Віднімає одну ціну від іншої."""
        return Price(self.amount - other.amount)

    def __eq__(self, other: object) -> bool:
        """Перевіряє рівність цін."""
        if not isinstance(other, Price):
            return NotImplemented
        return self.amount == other.amount

    def __lt__(self, other: "Price") -> bool:
        """Перевіряє, чи менша ціна."""
        return self.amount < other.amount

    def __le__(self, other: "Price") -> bool:
        """Менше або дорівнює."""
        return self.amount <= other.amount

    def __gt__(self, other: "Price") -> bool:
        """Більше."""
        return self.amount > other.amount

    def __ge__(self, other: "Price") -> bool:
        """Більше або дорівнює."""
        return self.amount >= other.amount

    def __repr__(self) -> str:
        """Повертає текстове представлення ціни."""
        return f"Price({str(self.amount)} грн)"

    def as_decimal(self) -> Decimal:
        """Повертає ціну як Decimal."""
        return self.amount


# ---------------------------------
p1 = Price(10.123)
p2 = Price("5.499")

print(p1)  # Price(10.12 грн)
print(p2)  # Price(5.50 грн)
print(p1 + p2)  # Price(15.62 грн)
print(p1 - p2)  # Price(4.62 грн)
print(p1 > p2)  # True

#
# Округления:
# Название	            Поведение
# ROUND_HALF_UP	        Классическое округление (0.5 → вверх)
# ROUND_DOWN	        Всегда вниз
# ROUND_UP	            Всегда вверх
# ROUND_HALF_EVEN	    Банковское округление
