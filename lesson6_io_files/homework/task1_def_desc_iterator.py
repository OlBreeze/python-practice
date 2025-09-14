# 1. Створення власного ітератора для зворотного читання файлу
# Напишіть власний ітератор, який буде зчитувати файл у зворотному порядку — рядок за рядком з кінця файлу до початку.
# Це може бути корисно для аналізу лог-файлів, коли останні записи найважливіші.
def file_reader(filename):
    """
        Ітератор для зворотного читання файлу у текстовому режимі.
        """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in reversed(lines):
                yield line.rstrip('\n')
    except FileNotFoundError:
        print(f"Файл {filename} не знайдено")
    except Exception as ex:
        print(f"Сталася помилка: {ex}")


# ------------------------------------------------
file_name = 'task1.txt'
for line in file_reader(file_name):
    print(line)
