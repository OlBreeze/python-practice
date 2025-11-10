# Завдання 2: Менеджер підписки на розсилку
from typing import List

subscribers: List[str] = []


def subscribe(name: str) -> None:
    """
    Додає користувача до списку підписників і підтверджує підписку.
    Parameters
    ----------
    name : str
    Ім'я користувача, якого потрібно підписати.
    """
    subscribers.append(name)

    def confirm_subscription():
        """
        Локальна функція для підтвердження підписки.
        Використовує замикання, щоб звернутися до змінної name
        із зовнішньої області видимості.
        """
        print(f"Підписка підтверджена для {name}")

    return confirm_subscription()


def unsubscribe(name: str):
    """Функція для відписки користувача від розсилки."""
    if name in subscribers:
        subscribers.remove(name)
        print(f"{name} успішно відписаний")
    else:
        print(f"Підписника {name} не знайдено у списку")


subscribe("Олена")
subscribe("Ігор")
print(subscribers)

unsubscribe("Ігор")
print(subscribers)

unsubscribe("Ivan")
