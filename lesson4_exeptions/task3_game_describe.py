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

from typing import Dict, Any, Union, Optional
from enum import Enum
import logging


class EventType(Enum):
    """Перелік типів ігрових подій."""
    DEATH = "death"
    LEVEL_UP = "levelUp"
    ITEM_FOUND = "itemFound"
    QUEST_COMPLETED = "questCompleted"
    ACHIEVEMENT_UNLOCKED = "achievementUnlocked"
    BATTLE_WON = "battleWon"
    BATTLE_LOST = "battleLost"


class ResourceType(Enum):
    """Перелік типів ресурсів у грі."""
    HEALTH = "health"
    MANA = "mana"
    GOLD = "gold"
    EXPERIENCE = "experience"
    STAMINA = "stamina"
    ENERGY = "energy"


class GameEventException(Exception):
    """
    Виключення для обробки різноманітних ігрових подій.

    Це виключення використовується для передачі інформації про ігрові події
    через механізм винятків, дозволяючи централізовано обробляти всі ігрові події.
    """

    def __init__(
            self,
            event_type: Union[str, EventType],
            details: Optional[Dict[str, Any]] = None,
            message: Optional[str] = None
    ) -> None:
        """
        Ініціалізує новий екземпляр GameEventException.

        Args:
            event_type: Тип події (рядок або EventType enum)
            details: Словник з додатковою інформацією про подію
            message: Повідомлення про подію (опціонально)
        """
        self.event_type = event_type.value if isinstance(event_type, EventType) else event_type
        self.details = details or {}

        # Формуємо повідомлення автоматично, якщо воно не надане
        if message is None:
            message = self._generate_message()

        super().__init__(message)

    def _generate_message(self) -> str:
        """
        Генерує автоматичне повідомлення на основі типу події та деталей.

        Returns:
            Сформоване повідомлення про подію
        """
        base_message = f"Ігрова подія: {self.event_type}"

        if self.details:
            details_str = ", ".join([f"{key}: {value}" for key, value in self.details.items()])
            return f"{base_message} ({details_str})"

        return base_message

    def get_event_info(self) -> Dict[str, Any]:
        """
        Повертає повну інформацію про подію.

        Returns:
            Словник з інформацією про подію
        """
        return {
            "event_type": self.event_type,
            "details": self.details,
            "message": str(self),
            "timestamp": None  # Можна додати реальний час
        }


class InsufficientResourcesException(Exception):
    """
    Виключення для обробки ситуацій недостатніх ресурсів.

    Використовується коли гравець намагається виконати дію,
    для якої у нього недостатньо ресурсів.
    """

    def __init__(
            self,
            resource_type: Union[str, ResourceType],
            required_amount: Union[int, float],
            current_amount: Union[int, float],
            action: Optional[str] = None
    ) -> None:
        """
        Ініціалізує новий екземпляр InsufficientResourcesException.

        Args:
            resource_type: Тип ресурсу, якого не вистачає
            required_amount: Необхідна кількість ресурсу
            current_amount: Поточна кількість ресурсу
            action: Дія, яку намагався виконати гравець (опціонально)
        """
        self.resource_type = resource_type.value if isinstance(resource_type, ResourceType) else resource_type
        self.required_amount = required_amount
        self.current_amount = current_amount
        self.deficit = required_amount - current_amount
        self.action = action

        message = self._generate_message()
        super().__init__(message)

    def _generate_message(self) -> str:
        """
        Генерує повідомлення про нестачу ресурсів.

        Returns:
            Сформоване повідомлення про нестачу ресурсів
        """
        base_message = (f"Недостатньо ресурсу '{self.resource_type}': "
                        f"потрібно {self.required_amount}, "
                        f"є {self.current_amount} "
                        f"(не вистачає {self.deficit})")

        if self.action:
            return f"{base_message}. Дія: {self.action}"

        return base_message

    def get_resource_info(self) -> Dict[str, Any]:
        """
        Повертає повну інформацію про нестачу ресурсу.

        Returns:
            Словник з інформацією про ресурс
        """
        return {
            "resource_type": self.resource_type,
            "required_amount": self.required_amount,
            "current_amount": self.current_amount,
            "deficit": self.deficit,
            "action": self.action
        }


class GameEventHandler:
    """
    Клас для централізованої обробки ігрових подій.

    Забезпечує логування подій та можливість додавання
    користувацьких обробників для різних типів подій.
    """

    def __init__(self) -> None:
        """Ініціалізує обробник ігрових подій."""
        self.logger = logging.getLogger(__name__)
        self._event_handlers: Dict[str, list] = {}
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Налаштовує логування для ігрових подій."""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def add_event_handler(self, event_type: str, handler_func) -> None:
        """
        Додає обробник для конкретного типу події.

        Args:
            event_type: Тип події
            handler_func: Функція-обробник
        """
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        self._event_handlers[event_type].append(handler_func)

    def handle_game_event(self, exception: GameEventException) -> None:
        """
        Обробляє ігрову подію.

        Args:
            exception: Екземпляр GameEventException
        """
        event_info = exception.get_event_info()

        # Логуємо подію
        self.logger.info(f"Обробка події: {exception}")

        # Викликаємо користувацькі обробники
        if exception.event_type in self._event_handlers:
            for handler in self._event_handlers[exception.event_type]:
                try:
                    handler(event_info)
                except Exception as e:
                    self.logger.error(f"Помилка в обробнику події: {e}")

    def handle_resource_exception(self, exception: InsufficientResourcesException) -> None:
        """
        Обробляє виключення нестачі ресурсів.

        Args:
            exception: Екземпляр InsufficientResourcesException
        """
        resource_info = exception.get_resource_info()

        # Логуємо нестачу ресурсів
        self.logger.warning(f"Нестача ресурсів: {exception}")

        # Тут можна додати логіку для відновлення або пропозиції альтернатив


# Приклад використання
class GameSimulator:
    """
    Симулятор гри для демонстрації роботи з подіями та ресурсами.
    """

    def __init__(self) -> None:
        """Ініціалізує симулятор гри."""
        self.event_handler = GameEventHandler()
        self.player_resources = {
            ResourceType.HEALTH.value: 100,
            ResourceType.MANA.value: 50,
            ResourceType.GOLD.value: 25,
            ResourceType.EXPERIENCE.value: 1500
        }
        self.player_level = 5

        # Додаємо обробники подій
        self._setup_event_handlers()

    def _setup_event_handlers(self) -> None:
        """Налаштовує обробники для різних типів подій."""

        def handle_death(event_info: Dict[str, Any]) -> None:
            print(f"💀 Гравець загинув! Причина: {event_info['details'].get('cause', 'Невідома')}")

        def handle_level_up(event_info: Dict[str, Any]) -> None:
            print(f"🎉 Підвищення рівня до {event_info['details'].get('new_level', 'N/A')}!")

        def handle_item_found(event_info: Dict[str, Any]) -> None:
            item_name = event_info['details'].get('item_name', 'Невідомий предмет')
            print(f"✨ Знайдено предмет: {item_name}")

        self.event_handler.add_event_handler(EventType.DEATH.value, handle_death)
        self.event_handler.add_event_handler(EventType.LEVEL_UP.value, handle_level_up)
        self.event_handler.add_event_handler(EventType.ITEM_FOUND.value, handle_item_found)

    def player_dies(self, cause: str = "Невідома причина") -> None:
        """
        Симулює смерть гравця.

        Args:
            cause: Причина смерті
        """
        try:
            raise GameEventException(
                event_type=EventType.DEATH,
                details={
                    "cause": cause,
                    "location": "Темний ліс",
                    "level_lost": self.player_level
                }
            )
        except GameEventException as e:
            self.event_handler.handle_game_event(e)

    def player_levels_up(self, experience_gained: int) -> None:
        """
        Симулює підвищення рівня гравця.

        Args:
            experience_gained: Кількість отриманого досвіду
        """
        try:
            self.player_level += 1
            raise GameEventException(
                event_type=EventType.LEVEL_UP,
                details={
                    "new_level": self.player_level,
                    "experience_gained": experience_gained,
                    "total_experience": self.player_resources[ResourceType.EXPERIENCE.value] + experience_gained
                }
            )
        except GameEventException as e:
            self.event_handler.handle_game_event(e)

    def find_item(self, item_name: str, item_value: int) -> None:
        """
        Симулює знаходження предмету.

        Args:
            item_name: Назва предмету
            item_value: Вартість предмету
        """
        try:
            raise GameEventException(
                event_type=EventType.ITEM_FOUND,
                details={
                    "item_name": item_name,
                    "item_value": item_value,
                    "rarity": "Epic" if item_value > 100 else "Common"
                }
            )
        except GameEventException as e:
            self.event_handler.handle_game_event(e)

    def cast_spell(self, mana_cost: int, spell_name: str) -> None:
        """
        Симулює використання заклинання.

        Args:
            mana_cost: Вартість заклинання в мані
            spell_name: Назва заклинання
        """
        current_mana = self.player_resources[ResourceType.MANA.value]

        if current_mana < mana_cost:
            try:
                raise InsufficientResourcesException(
                    resource_type=ResourceType.MANA,
                    required_amount=mana_cost,
                    current_amount=current_mana,
                    action=f"Використання заклинання '{spell_name}'"
                )
            except InsufficientResourcesException as e:
                self.event_handler.handle_resource_exception(e)
                print(f"❌ Не вдалося використати заклинання '{spell_name}'")
        else:
            self.player_resources[ResourceType.MANA.value] -= mana_cost
            print(f"✅ Заклинання '{spell_name}' успішно використано! "
                  f"Залишилось мани: {self.player_resources[ResourceType.MANA.value]}")

    def buy_item(self, item_cost: int, item_name: str) -> None:
        """
        Симулює покупку предмету.

        Args:
            item_cost: Вартість предмету
            item_name: Назва предмету
        """
        current_gold = self.player_resources[ResourceType.GOLD.value]

        if current_gold < item_cost:
            try:
                raise InsufficientResourcesException(
                    resource_type=ResourceType.GOLD,
                    required_amount=item_cost,
                    current_amount=current_gold,
                    action=f"Покупка предмету '{item_name}'"
                )
            except InsufficientResourcesException as e:
                self.event_handler.handle_resource_exception(e)
                print(f"💰 Не вдалося купити '{item_name}' - не вистачає золота!")
        else:
            self.player_resources[ResourceType.GOLD.value] -= item_cost
            print(f"🛍️ Предмет '{item_name}' успішно куплено! "
                  f"Залишилось золота: {self.player_resources[ResourceType.GOLD.value]}")


def demonstrate_game_events() -> None:
    """Демонстрація роботи системи ігрових подій."""
    print("=== Демонстрація системи ігрових подій ===\n")

    game = GameSimulator()

    print(f"Початкові ресурси гравця: {game.player_resources}")
    print(f"Рівень гравця: {game.player_level}\n")

    # Демонстрація різних подій
    print("1. Смерть гравця:")
    game.player_dies("Удар драконячого вогню")

    print("\n2. Підвищення рівня:")
    game.player_levels_up(500)

    print("\n3. Знаходження предмету:")
    game.find_item("Меч драконобійця", 150)

    print("\n4. Успішне використання заклинання:")
    game.cast_spell(30, "Вогняна куля")

    print("\n5. Неуспішне використання заклинання (не вистачає мани):")
    game.cast_spell(25, "Блискавка")

    print("\n6. Успішна покупка:")
    game.buy_item(20, "Зілля здоров'я")

    print("\n7. Неуспішна покупка (не вистачає золота):")
    game.buy_item(10, "Магічний еліксир")

    print(f"\nФінальні ресурси гравця: {game.player_resources}")
    print(f"Фінальний рівень гравця: {game.player_level}")


if __name__ == "__main__":
    demonstrate_game_events()