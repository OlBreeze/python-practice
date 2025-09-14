# Створити механізм обробки ситуацій, коли користувач намагається завершити операцію,
# для якої у нього недостатньо коштів на рахунку. Вимоги:
# Створити клас InsufficientFundsException, наступний від виключеного базового класу.
# Додайте наступні властивості:
# required_amount: грошова сума, необхідна для виконання операції.
# current_balance: поточний баланс рахунку.
# Опціонально:
# currency: валюта рахунку.
# transaction_type: тип транзакції (наприклад, "withdrawal", "purchase").
# Використання: При спробі завершити операцію, перевірити достатню кількість коштів на рахунку.
# Якщо коштів недостатньо, створіть екземпляр InsufficientFundsException з іншими значеннями
# властивостей і викиньте його.
# Опрацювати виключення, щоб повідомити користувача про брак коштів і припинити виконання операції.

from decimal import Decimal
from typing import Optional


class InsufficientFundsException(Exception):
    """
    Виключення, що виникає при спробі виконати операцію з недостатніми коштами.

    Attributes:
        required_amount (Decimal): Грошова сума, необхідна для виконання операції.
        current_balance (Decimal): Поточний баланс рахунку.
        currency (Optional[str]): Валюта рахунку (за замовчуванням None).
        transaction_type (Optional[str]): Тип транзакції (за замовчуванням None).
    """

    def __init__(
            self,
            required_amount: Decimal,
            current_balance: Decimal,
            currency: Optional[str] = None,
            transaction_type: Optional[str] = None,
            message: Optional[str] = None
    ) -> None:
        """Ініціалізація виключення InsufficientFundsException."""
        self.required_amount = required_amount
        self.current_balance = current_balance
        self.currency = currency
        self.transaction_type = transaction_type

        if message is None:
            currency_str = f" {self.currency}" if self.currency else ""
            transaction_str = f" для операції '{self.transaction_type}'" if self.transaction_type else ""
            message = (
                f"Недостатньо коштів{transaction_str}. "
                f"Необхідно: {self.required_amount}{currency_str}, "
                f"доступно: {self.current_balance}{currency_str}"
            )

        super().__init__(message)


class BankAccount:
    """
    Клас банківського рахунку з механізмом перевірки достатності коштів.

    Attributes:
        balance (Decimal): Поточний баланс рахунку.
        currency (str): Валюта рахунку.
    """

    def __init__(self, initial_balance: Decimal = Decimal('0'), currency: str = 'UAH') -> None:
        """
        Ініціалізація банківського рахунку.

        Args:
            initial_balance (Decimal): Початковий баланс рахунку.
            currency (str): Валюта рахунку.
        """
        self._balance = initial_balance
        self.currency = currency

    def check_sufficient_funds(self, required_amount: Decimal, transaction_type: str = None) -> None:
        """
        Перевіряє достатність коштів на рахунку для виконання операції.

        Args:
            required_amount (Decimal): Необхідна сума для операції.
            transaction_type (str): Тип транзакції.

        Raises:
            InsufficientFundsException: Якщо коштів недостатньо для операції.
        """
        if self._balance < required_amount:
            raise InsufficientFundsException(
                required_amount=required_amount,
                current_balance=self._balance,
                currency=self.currency,
                transaction_type=transaction_type
            )

    def withdraw(self, amount: Decimal) -> None:
        """
        Зняття коштів з рахунку.

        Args:
            amount (Decimal): Сума для зняття.

        Raises:
            InsufficientFundsException: Якщо коштів недостатньо для зняття.
        """
        self.check_sufficient_funds(amount, "withdrawal")
        self._balance -= amount
        print(f"Знято {amount} {self.currency}. Поточний баланс: {self._balance} {self.currency}")

    def purchase(self, amount: Decimal) -> None:
        """
        Здійснення покупки.

        Args:
            amount (Decimal): Сума покупки.

        Raises:
            InsufficientFundsException: Якщо коштів недостатньо для покупки.
        """
        self.check_sufficient_funds(amount, "purchase")
        self._balance -= amount
        print(f"Покупка на суму {amount} {self.currency} здійснена. Поточний баланс: {self._balance} {self.currency}")

    def deposit(self, amount: Decimal) -> None:
        """Поповнення рахунку."""
        self._balance += amount
        print(f"Рахунок поповнено на {amount} {self.currency}. Поточний баланс: {self._balance} {self.currency}")

    def get_balance(self) -> Decimal:
        """Отримання поточного балансу рахунку."""
        return self._balance


# Приклад використання
if __name__ == "__main__":
    # Створення рахунку з початковим балансом
    account = BankAccount(Decimal('1000'), 'UAH')
    print(f"Початковий баланс: {account.get_balance()} {account.currency}")
    print()

    # Успішна операція зняття
    print("--- Спроба зняти 500 UAH ---")
    try:
        account.withdraw(Decimal('500'))
        print("Операція успішна")
    except InsufficientFundsException as e:
        print(f"ПОМИЛКА: {e}")
        shortage = e.required_amount - e.current_balance
        print(f"Бракує коштів: {shortage} {e.currency}")
    print()

    # Успішна операція покупки
    print("--- Спроба здійснити покупку на 300 UAH ---")
    try:
        account.purchase(Decimal('300'))
        print("Операція успішна")
    except InsufficientFundsException as e:
        print(f"ПОМИЛКА: {e}")
        shortage = e.required_amount - e.current_balance
        print(f"Бракує коштів: {shortage} {e.currency}")
    print()

    # Неуспішна операція - недостатньо коштів
    print("--- Спроба зняти 500 UAH (недостатньо коштів) ---")
    try:
        account.withdraw(Decimal('500'))
        print("Операція успішна")
    except InsufficientFundsException as e:
        print(f"ПОМИЛКА: {e}")
        shortage = e.required_amount - e.current_balance
        print(f"Бракує коштів: {shortage} {e.currency}")
    print()

    # Демонстрація прямого використання виключення
    print("--- Пряме використання виключення ---")
    try:
        account.check_sufficient_funds(Decimal('1000'), 'transfer')
    except InsufficientFundsException as e:
        print(f"Перехоплено виключення: {e}")
        print(f"Необхідна сума: {e.required_amount} {e.currency}")
        print(f"Поточний баланс: {e.current_balance} {e.currency}")
        print(f"Тип транзакції: {e.transaction_type}")
