# 8. Конфігурація через контекстні менеджери
# Напишіть власний контекстний менеджер для роботи з файлом конфігурацій (формат .ini або .json).
# Менеджер має автоматично зчитувати конфігурацію при вході в контекст і записувати зміни в файл
# після завершення роботи.

import configparser
from typing import Any


class INIConfigManager:
    """
    Контекстний менеджер для роботи з INI-файлом конфігурацій.

    Автоматично зчитує дані при вході в контекст та зберігає
    зміни назад у файл при виході.
    """

    def __init__(self, filepath: str) -> None:
        """
        Ініціалізує менеджер конфігурацій.

        :param filepath: Шлях до INI-файлу з конфігурацією.
        """
        self.filepath: str = filepath
        self.config: configparser.ConfigParser = configparser.ConfigParser()

    def __enter__(self) -> configparser.ConfigParser:
        """
        Вхід у контекст: відкриває файл і завантажує конфігурацію.

        :return: Об'єкт ConfigParser для роботи з параметрами.
        """
        self.config.read(self.filepath, encoding="utf-8")
        return self.config

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Вихід з контексту: зберігає оновлену конфігурацію назад у файл.

        :param exc_type: Тип виключення (якщо сталося).
        :param exc_val: Значення виключення.
        :param exc_tb: Трасування виключення.
        """
        with open(self.filepath, "w", encoding="utf-8") as f:
            self.config.write(f)


# ==================================

if __name__ == "__main__":
    config_path = "task8_files/settings.ini"

    # Працюємо з конфігурацією через контекстний менеджер
    with INIConfigManager(config_path) as cfg:
        # Якщо секція відсутня — треба додати
        if "User" not in cfg:
            cfg["User"] = {}
        cfg["User"]["username"] = "Olga"
        cfg["User"]["theme"] = "dark"
        cfg["User"]["font_size"] = "14"

    # Після виходу з контексту зміни автоматично збережено
    with INIConfigManager(config_path) as cfg:
        print("Конфігурація після змін:")
        for section in cfg.sections():
            print(f"[{section}]")
            for key, value in cfg[section].items():
                print(f"{key} = {value}")
