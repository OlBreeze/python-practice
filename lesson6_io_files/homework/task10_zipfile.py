# 10. Архівування та зберігання великих даних
# Реалізуйте менеджер контексту для архівування файлів (за допомогою модуля zipfile).
# Менеджер автоматично створює архів, додає файли, а після виходу з блоку with –
# завершує архівування та закриває архів.

import zipfile
import os
from typing import List, Optional


class ZipArchiver:
    """
    Контекстний менеджер для архівування файлів у форматі ZIP.

    Можливості:
      - Додавати окремі файли (`add_file`).
      - Додавати цілу директорію рекурсивно (`add_dir`).
      - Передати список файлів при створенні архіватора.
    Після виходу з контексту архів автоматично закривається.
    """

    def __init__(
        self,
        archive_name: str,
        files: Optional[List[str]] = None,
        mode: str = "w",
        compression: int = zipfile.ZIP_DEFLATED
    ) -> None:
        """
        Ініціалізує архіватор.

        :param archive_name: Назва архіву (наприклад, "data.zip").
        :param files: Список файлів для архівування (за замовчуванням None).
        :param mode: Режим відкриття архіву: "w" – створення нового, "a" – додавання.
        :param compression: Алгоритм стиснення (за замовчуванням ZIP_DEFLATED).
        """
        self.archive_name: str = archive_name
        self.files: List[str] = files if files is not None else []
        self.mode: str = mode
        self.compression: int = compression
        self._zip: Optional[zipfile.ZipFile] = None

    def __enter__(self) -> "ZipArchiver":
        """Відкриває архів для запису і додає файли зі списку (якщо вони є)."""
        self._zip = zipfile.ZipFile(self.archive_name, mode=self.mode, compression=self.compression)

        # якщо передано список файлів – додати їх усі
        for file_path in self.files:
            self.add_file(file_path)

        return self

    def add_file(self, file_path: str, arcname: Optional[str] = None) -> None:
        """
        Додає файл до архіву.

        :param file_path: Шлях до файлу на диску.
        :param arcname: Ім’я файлу в архіві (якщо None – береться з file_path).
        """
        if not self._zip:
            raise RuntimeError("Архів ще не відкрито. Використовуйте в блоці 'with'.")
        self._zip.write(file_path, arcname=arcname)

    def add_dir(self, dir_path: str, arcname: Optional[str] = None) -> None:
        """
        Додає усю директорію рекурсивно до архіву.

        :param dir_path: Шлях до директорії.
        :param arcname: Базова директорія в архіві (якщо None – береться ім’я dir_path).
        """
        if not self._zip:
            raise RuntimeError("Архів ще не відкрито. Використовуйте в блоці 'with'.")

        base_arcname = arcname if arcname else os.path.basename(dir_path)

        for root, _, files in os.walk(dir_path):
            for file in files:
                full_path = os.path.join(root, file)
                # обчислюємо відносний шлях у архіві
                rel_path = os.path.relpath(full_path, start=dir_path)
                archive_path = os.path.join(base_arcname, rel_path)
                self._zip.write(full_path, arcname=archive_path)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Закриває архів після виходу з контексту."""
        if self._zip:
            self._zip.close()

#--------------------------------------------------------------
# #Архівація файлів зі списку
# with ZipArchiver("batch_archive.zip", files=["file1.txt", "file2.txt"]):
#     pass  # файли вже додані
#
# #Додавання файлів вручну
# with ZipArchiver("manual_archive.zip") as archiver:
#     archiver.add_file("notes.txt")
#     archiver.add_file("report.pdf", arcname="final_report.pdf")

#Додавання цілої директорії йооохооо!!!
with ZipArchiver("project_backup.zip") as archiver:
    archiver.add_dir(".")  # архівує всі файли та піддиректорії
