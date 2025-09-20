import requests

from lesson8_tests.homework.task6.my_exceptions import InvalidAmountError, InsufficientFundsError


class BankAccount:
    """Клас для роботи з банківським рахунком"""

    def __init__(self, account_number: str, initial_balance: float = 0.0):
        """
        Ініціалізація банківського рахунку

        Args:
            account_number: номер рахунку
            initial_balance: початковий баланс
        """
        if initial_balance < 0:
            raise InvalidAmountError("Початковий баланс не може бути від'ємним")

        self.account_number = account_number
        self._balance = initial_balance

    def deposit(self, amount: float) -> float:
        """
        Поповнення рахунку

        Args:
            amount: сума для поповнення

        Returns:
            Новий баланс рахунку

        Raises:
            InvalidAmountError: якщо сума некоректна
        """
        if amount <= 0:
            raise InvalidAmountError("Сума поповнення повинна бути позитивною")

        self._balance += amount
        return self._balance

    def withdraw(self, amount: float) -> float:
        """
        Зняття коштів з рахунку

        Args:
            amount: сума для зняття

        Returns:
            Новий баланс рахунку

        Raises:
            InvalidAmountError: якщо сума некоректна
            InsufficientFundsError: якщо недостатньо коштів
        """
        if amount <= 0:
            raise InvalidAmountError("Сума зняття повинна бути позитивною")

        if amount > self._balance:
            raise InsufficientFundsError(
                f"Недостатньо коштів. Баланс: {self._balance}, запитувана сума: {amount}"
            )

        self._balance -= amount
        return self._balance

    def get_balance(self) -> float:
        """Повертає поточний баланс рахунку"""
        return self._balance

    def verify_balance_with_api(self, api_url: str) -> bool:
        """
        Перевіряє баланс через зовнішній API

        Args:
            api_url: URL API для перевірки

        Returns:
            True, якщо баланс підтверджено
        """
        try:
            response = requests.post(
                api_url,
                json={
                    'account_number': self.account_number,
                    'balance': self._balance
                },
                timeout=5
            )
            return response.status_code == 200 and response.json().get('verified', False)
        except requests.RequestException:
            return False
