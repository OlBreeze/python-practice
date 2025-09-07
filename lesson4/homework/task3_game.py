# 3. Створити гнучкий механізм для обробки різноманітних ігрових подій, надаючи детальну інформацію
# про події, що відбулися.
# Вимоги:
# Створити клас GameEventException, наступний від базового класу.
# Додайте наступні властивості:
# event_type: рядок, який описує тип події (наприклад, "death", "levelUp").
# details: словник або об'єкт, що містить додаткову інформацію про події.
# Наприклад:
#
# Для події "смерть": причина смерті (удар мечем, падіння).
#
# Для події "levelUp": новий рівень персонажу, отримані очки досвіду.
#
# Використання:
#
# Після закінчення ігрової події створіть екземпляр GameEventException з іншими значеннями властивостей.
#
# Викинути це виключення з коду гри.
#
# Обробка виключення в загальному блоці try-catch або в більш специфічному обробнику, щоб виконати необхідні дії
# (наприклад, показати повідомлення користувачеві, зберегти дані про події).
# 4. Створити механізм для обробки ситуацій, коли гравецю не вистачає ресурсів для виконання дій.

from typing import Dict, Any, Union


class GameEventException(Exception):
    """
    Виключення для обробки різноманітних ігрових подій.
    Надає детальну інформацію про події, що відбулися в грі.
    """

    def __init__(self, event_type: str, details: Dict[str, Any]) -> None:
        """
        Ініціалізує новий екземпляр GameEventException.

        Args:
            event_type: Тип події (наприклад, "death", "levelUp")
            details: Словник з додатковою інформацією про подію
        """
        self.event_type = event_type
        self.details = details

        message = f"Ігрова подія: {event_type}"
        super().__init__(message)


# Приклади використання
def simulate_death_event() -> None:
    """Демонстрація події смерті."""
    try:
        # Створення екземпляру GameEventException для події смерті
        raise GameEventException(
            event_type="death",
            details={
                "причина_смерті": "удар мечем",
                "локація": "темний ліс",
                "рівень_персонажа": 5
            }
        )
    except GameEventException as e:
        # Обробка виключення
        print(f"Подія: {e.event_type}")
        print(f"Деталі: {e.details}")
        print(f"Повідомлення: {e}")

        # Виконання необхідних дій
        print("Дії: відновлення персонажа на респауні")


def simulate_level_up_event() -> None:
    """Демонстрація події підвищення рівня."""
    try:
        # Створення екземпляру GameEventException для події levelUp
        raise GameEventException(
            event_type="levelUp",
            details={
                "новий_рівень": 6,
                "отримані_очки_досвіду": 1500,
                "нові_навички": ["вогняна_куля", "лікування"]
            }
        )
    except GameEventException as e:
        # Обробка виключення
        print(f"\nПодія: {e.event_type}")
        print(f"Деталі: {e.details}")
        print(f"Повідомлення: {e}")

        # Виконання необхідних дій
        print("Дії: показано повідомлення про підвищення рівня")


def demonstrate_general_exception_handling() -> None:
    """Демонстрація загальної обробки виключень."""
    events_to_simulate = [
        ("death", {"причина_смерті": "падіння з висоти", "висота": "50 метрів"}),
        ("levelUp", {"новий_рівень": 10, "отримані_очки_досвіду": 2000}),
        ("questCompleted", {"назва_квесту": "Врятувати принцесу", "нагорода": 500})
    ]

    print("\n--- Загальна обробка різних подій ---")

    for event_type, details in events_to_simulate:
        try:
            raise GameEventException(event_type, details)
        except GameEventException as e:
            # Загальний обробник для всіх ігрових подій
            print(f"\nОброблено подію: {e.event_type}")
            print(f"З деталями: {e.details}")

            # Різні дії залежно від типу події
            if e.event_type == "death":
                print("→ Збережено дані про смерть, повернення до респауну")
            elif e.event_type == "levelUp":
                print("→ Оновлено статистику персонажа, показано анімацію")
            elif e.event_type == "questCompleted":
                print("→ Видано нагороду, оновлено журнал квестів")


#-----------------------------------------
# Демонстрація події смерті
simulate_death_event()

# Демонстрація події підвищення рівня
simulate_level_up_event()

# Загальна обробка подій
demonstrate_general_exception_handling()
