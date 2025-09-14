# 8. Конфігурація через контекстні менеджери
# Напишіть власний контекстний менеджер для роботи з файлом конфігурацій (формат .ini або .json).
# Менеджер має автоматично зчитувати конфігурацію при вході в контекст і записувати зміни в файл
# після завершення роботи.

import json
from typing import Any, Dict


class ConfigManager:
    """
    Контекстний менеджер для роботи з JSON-файлом конфігурацій.

    Автоматично зчитує дані при вході в контекст та зберігає
    зміни назад у файл при виході.
    """

    def __init__(self, filepath: str) -> None:
        """
        Ініціалізує менеджер конфігурацій.

        :param filepath: Шлях до JSON-файлу з конфігурацією.
        """
        self.filepath: str = filepath
        self.config: Dict[str, Any] = {}

    def __enter__(self) -> Dict[str, Any]:
        """
        Вхід у контекст: відкриває файл і завантажує конфігурацію.

        :return: Словник з параметрами конфігурації.
        """
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            # Якщо файл не існує — створюємо новий з порожнім словником
            self.config = {}
        return self.config

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Вихід з контексту: зберігає оновлену конфігурацію назад у файл.

        :param exc_type: Тип виключення (якщо сталося).
        :param exc_val: Значення виключення.
        :param exc_tb: Трасування виключення.
        """
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)


# ================= Приклад  =================

if __name__ == "__main__":
    config_path = "task8_files/config.json"

    # Працюємо з конфігурацією через контекстний менеджер
    with ConfigManager(config_path) as cfg:
        print("Поточна конфігурація:", cfg)

        # Змінюємо або додаємо нові параметри
        cfg["username"] = "Olga"
        cfg["theme"] = "dark"
        cfg["font_size"] = 18

    # Після виходу з контексту зміни автоматично збережено
    with ConfigManager(config_path) as cfg:
        print("Оновлена конфігурація:", cfg)
