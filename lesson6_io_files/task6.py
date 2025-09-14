def file_reader(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for lines in file:
                yield lines
    except FileNotFoundError:
        print(f"Файл {filename} не знайдено")
    except Exception as ex:
        print(f"Сталася помилка: {ex}")

file_name = 'text.txt'

for line in file_reader(file_name):
    print(line)