# Завдання 2: Менеджер підписки на розсилку

subscribers = []


def subscribe(name: str):
    """
    Функція для підписки користувача на розсилку.
    """
    subscribers.append(name)

    def confirm_subscription():
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
