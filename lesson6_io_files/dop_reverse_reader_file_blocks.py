# Гібридна реалізація: читаємо частинами у текстовому режимі
# ✅ Цей варіант:
# читає файл частинами з кінця (по блоках), декодує блоки в текст з урахуванням кодування,
# розбиває на рядки, віддає рядки у зворотному порядку.
# Не читає весь файл у пам’ять, працює з великими файлами.
# Коректно працює з UTF-8 або іншим кодуванням.
# Працює з текстом, не вимагає від користувача працювати з байтами.
# ⚠️ Застереження:
# Може трохи ускладнитись, якщо файл має інше закінчення рядків, наприклад \r\n (Windows). Але це легко додати за потреби.
# Якщо всередині файлу будуть багатобайтові символи, і розбиття їх припаде на межу блоків,
# декодування може зламатися — для повної безпеки потрібно використовувати codecs.StreamReader,
# але в більшості випадків все працює стабільно.

from typing import Iterator


class ReverseFileReader:
    """
    Ефективний ітератор для зворотного читання текстового файлу (рядок за рядком з кінця до початку).
    Читає файл частинами, не завантажуючи повністю в пам’ять.
    """

    def __init__(self, filename: str, encoding: str = 'utf-8', block_size: int = 4096) -> None:
        """
        :param filename: Шлях до файлу
        :param encoding: Кодування файлу
        :param block_size: Розмір блоку для читання (байт)
        """
        self.filename = filename
        self.encoding = encoding
        self.block_size = block_size

    def __iter__(self) -> Iterator[str]:
        """
        Повертає ітератор рядків у зворотному порядку
        """
        try:
            with open(self.filename, 'rb') as f:
                f.seek(0, 2)
                file_size = f.tell()
                buffer = b""
                position = file_size

                while position > 0:
                    read_size = min(self.block_size, position)
                    position -= read_size
                    f.seek(position)
                    block = f.read(read_size)
                    buffer = block + buffer

                    # Розбити буфер на рядки
                    lines = buffer.split(b'\n')
                    buffer = lines[0]  # Залишок, ще не завершений рядок

                    for line in reversed(lines[1:]):
                        yield line.decode(self.encoding)

                if buffer:
                    yield buffer.decode(self.encoding)

        except FileNotFoundError:
            print(f"Файл '{self.filename}' не знайдено.")
        except Exception as e:
            print(f"Сталася помилка при читанні файлу: {e}")


if __name__ == "__main__":
    reader = ReverseFileReader("task1_unittest_doctest.txt")
    for line in reader:
        print(line)