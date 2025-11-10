# 6. Access-like
# 1.	Реалізуйте клас User з атрибутами first_name, last_name, email.
#   Додайте методи для отримання та встановлення цих атрибутів через декоратор @property.
# 2.	Додайте методи для перевірки формату email-адреси.

import re


class User:
    """Клас для представлення користувача з ім'ям, прізвищем та електронною поштою."""

    def __init__(self, first_name: str, last_name: str, email: str) -> None:
        """Ініціалізація користувача."""
        self._first_name: str = first_name
        self._last_name: str = last_name
        self._email: str = email if self._validate_email(email) else "invalid@example.com"

    # ---------- FIRST NAME ----------

    @property
    def first_name(self) -> str:
        """Повертає ім'я користувача."""
        return self._first_name

    @first_name.setter
    def first_name(self, value: str) -> None:
        """Встановлює нове ім'я користувача."""
        self._first_name = value

    # ---------- LAST NAME ----------

    @property
    def last_name(self) -> str:
        """Повертає прізвище користувача."""
        return self._last_name

    @last_name.setter
    def last_name(self, value: str) -> None:
        """Встановлює нове прізвище користувача."""
        self._last_name = value

    # ---------- EMAIL ----------

    @property
    def email(self) -> str:
        """Повертає email користувача."""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """
        Встановлює email користувача після перевірки формату.
        Якщо формат некоректний — встановлює як 'invalid@example.com'.
        """
        if self._validate_email(value):
            self._email = value
        else:
            print("Некоректна адреса. Встановлено за замовчуванням.")
            self._email = "invalid@example.com"

    # ---------- VALIDATION ----------

    @staticmethod
    def _validate_email(email: str) -> bool:
        """
        Перевіряє формат email за допомогою регулярного виразу.

        :param email: Email для перевірки
        :return: True, якщо формат коректний
        """
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        return re.match(pattern, email) is not None

    def __repr__(self) -> str:
        """Повертає рядкове представлення користувача."""
        return f"User({self.first_name} {self.last_name}, {self.email})"


# -----------------------------------------
user = User("Олена", "Коваль", "olena.koval@gmail.com")
print(user)

user.first_name = "Ольга"
user.last_name = "Шевченко"
print(user)

user.email = "incorrect-email"
print("Email після помилки:", user.email)

user.email = "olga.shevchenko@mail.com"
print("Email після коректного введення:", user.email)

print(user)
# -----------------------------------------
# [\w\.-]+
# — Кусок до знака @ — имя пользователя.
# \w — любой буквенно-цифровой символ или подчёркивание ([a-zA-Z0-9_])
# \. — точка (. в regex — это спецсимвол, его нужно экранировать)
# \- — дефис (-, тоже экранируется внутри [])
# [ \w \. \- ] — разрешённые символы: буквы, цифры, _, ., -
# + — один или больше символов
# \w{2,} — зона домена: com, org, ua, net, info, online и т.п.
# \w — буква, цифра, подчёркивание
# {2,} — от 2 и более символов (например, ua → 2, online → 6)
