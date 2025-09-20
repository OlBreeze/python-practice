import os

from lesson8_tests.homework.task7.file_processor import FileProcessor

if __name__ == "__main__":
    # Приклад використання
    processor = FileProcessor()

    # Демонстрація роботи
    test_file = "example.txt"
    test_data = "Приклад роботи з файлами"

    try:
        processor.write_to_file(test_file, test_data)
        content = processor.read_from_file(test_file)
        print(f"Записано та прочитано: {content}")

        # Очищення
        if os.path.exists(test_file):
            os.remove(test_file)

    except Exception as e:
        print(f"Помилка: {e}")
