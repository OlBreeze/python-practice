# 4. Створити механізм для обробки ситуацій, коли гравецю не вистачає ресурсів для виконання дій.
# Вимоги:
# Створити клас InsufficientResourcesException, наступний від базового класу-вийнятку.
# Додайте наступні властивості:
#   required_resource: рядок, що вказує на бракуючий ресурс (наприклад, "золото", "мана").
#   required_amount: Число, що вказує потрібну кількість ресурсу.
#   current_amount: Число, що вказує поточну кількість ресурсів у гравця.
# Використання:
#
# При спробі виконати дію, необхідне ресурс, перевірити наявність достатньої кількості ресурсів.
#
# Якщо ресурсів недостатньо, створіть екземпляр InsufficientResourcesException і запустіть його.
#
# Опрацювати виключення, щоб повідомити гравцеві про брак ресурсів.
from typing import Union


class InsufficientResourcesException(Exception):
    """Виключення для обробки ситуацій, коли гравцю не вистачає ресурсів."""

    def __init__(
            self,
            required_resource: str,
            required: Union[int, float],
            current: Union[int, float]
    ) -> None:
        """
        Ініціалізує новий екземпляр InsufficientResourcesException.

        Args:
           required_resource: рядок, що вказує на бракуючий ресурс (наприклад, "золото", "мана")
            required: Необхідна кількість ресурсу
            current: Поточна кількість ресурсу
        """
        self.required_resource = required_resource
        self.required = required
        self.current = current

        message = f"Недостатньо ресурсу '{required_resource}': потрібно {required}, є {current}"
        super().__init__(message)


# Приклади використання
def simulate_insufficient_resources() -> None:
    """Демонстрація нестачі ресурсів."""
    try:
        # Перевірка наявності ресурсів перед дією
        current_mana = 30
        required_mana = 50

        if current_mana < required_mana:
            raise InsufficientResourcesException(
                required_resource="мана",
                required=required_mana,
                current=current_mana
            )

        # Якщо ресурсів достатньо, виконуємо дію
        print("Заклинання успішно використано!")

    except InsufficientResourcesException as e:
        # Обробка виключення нестачі ресурсів
        print(f"\nПомилка: {e}")
        print(f"Тип ресурсу: {e.required_resource}")
        print(f"Потрібно: {e.required}")
        print(f"Є: {e.current}")
        print(f"Не вистачає: {e.required - e.current}")

        # Виконання необхідних дій
        print("Дії: пропозиція купити зілля мани або використати інше заклинання")


# Демонстрація нестачі ресурсів
simulate_insufficient_resources()
