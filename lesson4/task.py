class InsufficientError(Exception):
    def __init__(self, message="Не вистачає коштів", balance=0):
        super().__init__(message)
        self.balance = balance

class BankAccount:
    def __init__(self, initial_amount):
        if initial_amount < 0:
            raise ValueError("Баланс від'ємний")
        self.__balance = initial_amount

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("Баланс менше 0")
        self.__balance += amount
        print(f"Поповнення на {amount:.2f}. Новий баланс {self.__balance:.2f}.")

    def withdraw(self, amount):
        if amount > self.__balance:
            raise InsufficientError(message=f"недостатньо коштів на рахунку. \nДоступно: {self.__balance:.2f}",
                                    balance=self.__balance)
        elif amount < 0:
            raise ValueError("Сума для зняття менше 0")
        else:
            self.__balance -= amount
            print(f"Знято {amount}. Новий баланс: {self.__balance:.2f}.")

    def get_balance(self):
        return self.__balance

try:
    account = BankAccount(100)
    print(f"Поточний баланс {account.get_balance():.2f}")
    account.deposit(200)
    account.withdraw(500)
except InsufficientError as ex:
    print(f"Помилка: {ex}")
except ValueError as ex:
    print(f"Помилка: {ex}")