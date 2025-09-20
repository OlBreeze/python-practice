"""
Модуль для роботи з файлами.

Містить клас FileProcessor для запису та читання файлів.
"""
import os


class FileProcessor:
    """
    Клас для обробки операцій з файлами.

    Надає методи для запису та читання даних з файлів.
    """

    @staticmethod
    def write_to_file(file_path: str, data: str, encoding: str = 'utf-8') -> None:
        """
        Записує дані у файл.

        Args:
            file_path (str): Шлях до файлу для запису
            data (str): Дані для запису у файл
            encoding (str): Кодування файлу (за замовчуванням utf-8)

        Raises:
            IOError: Якщо виникла помилка при записі у файл
            PermissionError: Якщо немає прав для запису у файл
        """
        try:
            # Створюємо директорію, якщо вона не існує
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            with open(file_path, 'w', encoding=encoding) as file:
                file.write(data)
        except (IOError, PermissionError) as e:
            raise IOError(f"Помилка при записі у файл {file_path}: {e}")

    @staticmethod
    def read_from_file(file_path: str, encoding: str = 'utf-8') -> str:
        """
        Читає дані з файлу.

        Args:
            file_path (str): Шлях до файлу для читання
            encoding (str): Кодування файлу (за замовчуванням utf-8)

        Returns:
            str: Вміст файлу

        Raises:
            FileNotFoundError: Якщо файл не знайдено
            IOError: Якщо виникла помилка при читанні файлу
            PermissionError: Якщо немає прав для читання файлу
        """
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл не знайдено: {file_path}")
        except (IOError, PermissionError) as e:
            raise IOError(f"Помилка при читанні файлу {file_path}: {e}")





