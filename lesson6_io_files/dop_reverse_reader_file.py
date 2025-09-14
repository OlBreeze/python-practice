# Файл відкривається у бінарному режимі ('rb'), бо це дозволяє точно пересуватися по байтах.
from typing import Iterator


class ReverseFileReader:
    """
    Ітератор для зворотного читання файлу рядок за рядком (від останнього до першого).

    Приклад використання:
        reader = ReverseFileReader("log.txt")
        for line in reader:
            print(line)
    """
    def __init__(self, filename: str, encoding: str = 'utf-8') -> None:
        """
        Ініціалізує ітератор.

        :param filename: Ім'я файлу, який потрібно читати.
        :param encoding: Кодування файлу (за замовчуванням 'utf-8').
        """
        self.filename = filename
        self.encoding = encoding

    def __iter__(self) -> Iterator[str]:
        """
        Повертає ітератор, який читає файл у зворотному порядку по рядках.

        :return: Ітератор рядків у зворотному порядку.
        """
        try:
            with open(self.filename, 'rb') as f:
                f.seek(0, 2)  # Переходимо в кінець файлу
                position = f.tell()
                buffer = b''
                while position > 0:
                    position -= 1
                    f.seek(position)
                    byte = f.read(1)
                    if byte == b'\n':
                        if buffer:
                            yield buffer[::-1].decode(self.encoding)
                            buffer = b''
                    else:
                        buffer += byte
                if buffer:
                    yield buffer[::-1].decode(self.encoding)
        except FileNotFoundError:
            print(f"Файл '{self.filename}' не знайдено.")
        except Exception as e:
            print(f"Сталася помилка при читанні файлу: {e}")


if __name__ == "__main__":
    file_name = 'task1.txt'
    reader = ReverseFileReader(file_name)

    for line in reader:
        print(line)

