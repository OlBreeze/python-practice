# 9. Автоматичне резервне копіювання
# Напишіть менеджер контексту, який буде створювати резервну копію важливого файлу перед його обробкою.
# Якщо обробка пройде успішно, оригінальний файл замінюється новим.
# У разі помилки резервна копія автоматично відновлюється.

import shutil
import os
from typing import Optional


class BackupFileManager:
    """
    Контекстний менеджер для автоматичного резервного копіювання файлу.

    При вході у контекст:
    - створюється резервна копія оригінального файлу з суфіксом `.bak`.

    При виході з контексту:
    - якщо не виникло винятків — замінює оригінальний файл новим;
    - якщо виникла помилка — відновлює оригінальний файл з резервної копії.

    Атрибути:
        filepath (str): шлях до файлу, який потрібно захистити.
        backup_path (Optional[str]): шлях до резервної копії (створюється автоматично).
        temp_path (str): шлях до тимчасового файлу, куди можна записувати нові дані.
    """

    def __init__(self, filepath: str):
        """
        Ініціалізація менеджера.

        Args:
            filepath (str): шлях до важливого файлу.
        """
        self.filepath: str = filepath
        self.backup_path: Optional[str] = None
        self.temp_path: str = filepath + ".tmp"

    def __enter__(self) -> str:
        """
        Створює резервну копію файлу і повертає шлях до тимчасового файлу,
        куди можна записувати змінені дані.

        Returns:
            str: шлях до тимчасового файлу для редагування.
        """
        if os.path.exists(self.filepath):
            self.backup_path = self.filepath + ".bak"
            shutil.copy2(self.filepath, self.backup_path)

        return self.temp_path

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Виконує логіку відновлення або заміни файлу після виходу з контексту.

        Args:
            exc_type: тип виключення (якщо було).
            exc_val: значення виключення.
            exc_tb: трасування виключення.

        Returns:
            bool: True, якщо виняток оброблений, False — якщо його треба підняти далі.
        """
        try:
            if exc_type is None:
                # Якщо немає помилки → замінюємо оригінал
                if os.path.exists(self.temp_path):
                    shutil.move(self.temp_path, self.filepath)
            else:
                # Якщо була помилка → відновлюємо резервну копію
                if self.backup_path and os.path.exists(self.backup_path):
                    shutil.move(self.backup_path, self.filepath)

                # Видаляємо тимчасовий файл, якщо він залишився
                if os.path.exists(self.temp_path):
                    os.remove(self.temp_path)
        finally:
            # Очищаємо резервну копію
            if self.backup_path and os.path.exists(self.backup_path):
                os.remove(self.backup_path)

        return False  # виняток, якщо був, не пригнічується


# ======================= ПРИКЛАД =======================

if __name__ == "__main__":
    filepath = "task9_files/important.txt"

    # Припустимо, ми хочемо безпечно оновити файл
    try:
        with BackupFileManager(filepath) as temp_file:
            # Записуємо нові дані у тимчасовий файл
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write("Оновлені важливі дані\n")
                # Розкоментуй наступний рядок, щоб перевірити відновлення:
                # raise RuntimeError("Помилка під час обробки")
        print("Файл успішно оновлено!")
    except Exception as e:
        print(f"Сталася помилка: {e}")
