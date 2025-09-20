import pytest
from unittest.mock import Mock, patch
import requests
from bank_account import BankAccount, InsufficientFundsError, InvalidAmountError


class TestBankAccount:
    """Тестовий клас для BankAccount"""

    # ========== ФІКСТУРИ ==========

    @pytest.fixture
    def empty_account(self):
        """Фікстура для створення порожнього рахунку"""
        return BankAccount("ACC001", 0.0)

    @pytest.fixture
    def account_with_balance(self):
        """Фікстура для створення рахунку з балансом"""
        return BankAccount("ACC002", 1000.0)

    @pytest.fixture
    def rich_account(self):
        """Фікстура для створення рахунку з великим балансом"""
        return BankAccount("ACC003", 10000.0)

    @pytest.fixture(params=[0, 100, 1000, 5000])
    def account_with_various_balances(self, request):
        """Параметризована фікстура для різних балансів"""
        return BankAccount(f"ACC{request.param}", request.param)

    # ========== ТЕСТИ ІНІЦІАЛІЗАЦІЇ ==========

    def test_account_creation_with_valid_balance(self):
        """Тест створення рахунку з валідним балансом"""
        account = BankAccount("ACC123", 500.0)
        assert account.account_number == "ACC123"
        assert account.get_balance() == 500.0

    def test_account_creation_with_negative_balance_raises_error(self):
        """Тест створення рахунку з від'ємним балансом"""
        with pytest.raises(InvalidAmountError):
            BankAccount("ACC123", -100.0)

    # ========== ТЕСТИ ПОПОВНЕННЯ ==========

    @pytest.mark.parametrize("initial_balance,deposit_amount,expected_balance", [
        (0, 100, 100),
        (500, 250, 750),
        (1000, 1500, 2500),
        (0.50, 0.25, 0.75),
        (999.99, 0.01, 1000.00)
    ])
    def test_deposit_various_amounts(self, initial_balance, deposit_amount, expected_balance):
        """Параметризований тест поповнення різними сумами"""
        account = BankAccount("ACC123", initial_balance)
        new_balance = account.deposit(deposit_amount)
        assert new_balance == expected_balance
        assert account.get_balance() == expected_balance

    def test_deposit_with_fixture(self, empty_account):
        """Тест поповнення з використанням фікстури"""
        balance = empty_account.deposit(200.0)
        assert balance == 200.0
        assert empty_account.get_balance() == 200.0

    @pytest.mark.parametrize("invalid_amount", [-100, 0, -0.01])
    def test_deposit_invalid_amounts_raise_error(self, empty_account, invalid_amount):
        """Тест поповнення некоректними сумами"""
        with pytest.raises(InvalidAmountError):
            empty_account.deposit(invalid_amount)

    # ========== ТЕСТИ ЗНЯТТЯ КОШТІВ ==========

    @pytest.mark.parametrize("initial_balance,withdraw_amount,expected_balance", [
        (1000, 100, 900),
        (500, 500, 0),
        (1500, 750, 750),
        (100.50, 50.25, 50.25),
        (1000.00, 999.99, 0.01)
    ])
    def test_withdraw_valid_amounts(self, initial_balance, withdraw_amount, expected_balance):
        """Параметризований тест зняття валідними сумами"""
        account = BankAccount("ACC123", initial_balance)
        new_balance = account.withdraw(withdraw_amount)
        assert abs(new_balance - expected_balance) < 0.001  # Для float порівняння
        assert abs(account.get_balance() - expected_balance) < 0.001

    def test_withdraw_with_sufficient_funds(self, account_with_balance):
        """Тест зняття коштів при достатньому балансі"""
        balance = account_with_balance.withdraw(300.0)
        assert balance == 700.0
        assert account_with_balance.get_balance() == 700.0

    @pytest.mark.skip(reason="Тест пропускається якщо рахунок порожній")
    def test_withdraw_from_empty_account_skipped(self, empty_account):
        """Цей тест буде пропущено для порожнього рахунку"""
        pass

    def test_withdraw_from_empty_account_conditional_skip(self, account_with_various_balances):
        """Умовний скіп для тестування зняття коштів"""
        if account_with_various_balances.get_balance() == 0:
            pytest.skip("Пропускаємо тест зняття коштів для порожнього рахунку")

        # Тестуємо зняття коштів тільки якщо баланс > 0
        withdraw_amount = min(100, account_with_various_balances.get_balance())
        expected_balance = account_with_various_balances.get_balance() - withdraw_amount
        new_balance = account_with_various_balances.withdraw(withdraw_amount)
        assert new_balance == expected_balance

    @pytest.mark.parametrize("balance,withdraw_amount", [
        (100, 150),
        (0, 1),
        (500, 500.01),
        (1000, 2000)
    ])
    def test_withdraw_insufficient_funds(self, balance, withdraw_amount):
        """Тест зняття коштів при недостатньому балансі"""
        account = BankAccount("ACC123", balance)
        with pytest.raises(InsufficientFundsError):
            account.withdraw(withdraw_amount)

    @pytest.mark.parametrize("invalid_amount", [-100, 0, -0.01])
    def test_withdraw_invalid_amounts(self, account_with_balance, invalid_amount):
        """Тест зняття некоректними сумами"""
        with pytest.raises(InvalidAmountError):
            account_with_balance.withdraw(invalid_amount)

    # ========== ТЕСТИ З МОКАМИ ==========

    @patch('bank_account.requests.post')
    def test_verify_balance_api_success(self, mock_post, account_with_balance):
        """Тест успішної перевірки балансу через API (з моком)"""
        # Налаштування мока
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'verified': True}
        mock_post.return_value = mock_response

        # Виконання тесту
        result = account_with_balance.verify_balance_with_api("https://api.bank.com/verify")

        # Перевірки
        assert result is True
        mock_post.assert_called_once_with(
            "https://api.bank.com/verify",
            json={
                'account_number': account_with_balance.account_number,
                'balance': account_with_balance.get_balance()
            },
            timeout=5
        )

    @patch('bank_account.requests.post')
    def test_verify_balance_api_failure(self, mock_post, account_with_balance):
        """Тест неуспішної перевірки балансу через API"""
        # Налаштування мока для помилки HTTP
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        result = account_with_balance.verify_balance_with_api("https://api.bank.com/verify")
        assert result is False

    @patch('bank_account.requests.post')
    def test_verify_balance_api_network_error(self, mock_post, account_with_balance):
        """Тест мережевої помилки при перевірці балансу"""
        # Налаштування мока для мережевої помилки
        mock_post.side_effect = requests.RequestException("Network error")

        result = account_with_balance.verify_balance_with_api("https://api.bank.com/verify")
        assert result is False

    @patch('bank_account.requests.post')
    @pytest.mark.parametrize("status_code,verified_status,expected_result", [
        (200, True, True),
        (200, False, False),
        (404, True, False),
        (500, True, False)
    ])
    def test_verify_balance_various_responses(self, mock_post, account_with_balance,
                                              status_code, verified_status, expected_result):
        """Параметризований тест різних відповідей API"""
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.json.return_value = {'verified': verified_status}
        mock_post.return_value = mock_response

        result = account_with_balance.verify_balance_with_api("https://api.bank.com/verify")
        assert result == expected_result

    # ========== ІНТЕГРАЦІЙНІ ТЕСТИ ==========

    def test_multiple_operations(self, empty_account):
        """Тест послідовності операцій"""
        # Поповнення
        empty_account.deposit(1000)
        assert empty_account.get_balance() == 1000

        # Зняття частини коштів
        empty_account.withdraw(300)
        assert empty_account.get_balance() == 700

        # Ще одне поповнення
        empty_account.deposit(200)
        assert empty_account.get_balance() == 900

        # Зняття всіх коштів
        empty_account.withdraw(900)
        assert empty_account.get_balance() == 0

    @pytest.mark.parametrize("operations", [
        [("deposit", 100), ("withdraw", 50), ("deposit", 25)],
        [("deposit", 1000), ("withdraw", 1000), ("deposit", 500)],
        [("deposit", 300), ("deposit", 200), ("withdraw", 100)]
    ])
    def test_operation_sequences(self, empty_account, operations):
        """Параметризований тест послідовностей операцій"""
        expected_balance = 0

        for operation, amount in operations:
            if operation == "deposit":
                empty_account.deposit(amount)
                expected_balance += amount
            elif operation == "withdraw":
                empty_account.withdraw(amount)
                expected_balance -= amount

            assert empty_account.get_balance() == expected_balance


# conftest.py - конфігурація pytest
import pytest


def pytest_configure(config):
    """Конфігурація pytest з кастомними маркерами"""
    config.addinivalue_line("markers", "slow: позначає повільні тести")
    config.addinivalue_line("markers", "integration: інтеграційні тести")
    config.addinivalue_line("markers", "api: тести API")


@pytest.fixture(scope="session")
def test_data():
    """Фікстура сесії для тестових даних"""
    return {
        "test_accounts": [
            {"number": "TEST001", "balance": 0},
            {"number": "TEST002", "balance": 1000},
            {"number": "TEST003", "balance": 5000}
        ]
    }