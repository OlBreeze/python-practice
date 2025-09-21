"""
Тести для модуля file_processor.

Використовує pytest з фікстурами та тимчасовими файлами.
"""

import pytest
import os
import tempfile
from file_processor import FileProcessor


class TestFileProcessor:
    """Тестовий клас для FileProcessor."""

    def test_file_write_read_basic(self, tmpdir):
        """
        Тест базового запису та читання файлу.

        Args:
            tmpdir: pytest фікстура для створення тимчасової директорії
        """
        file_path = tmpdir.join("testfile.txt")
        test_data = "Hello, World!"

        FileProcessor.write_to_file(str(file_path), test_data)
        content = FileProcessor.read_from_file(str(file_path))

        assert content == test_data

    def test_file_write_read_empty_string(self, tmpdir):
        """Тест запису та читання порожнього рядка."""
        file_path = tmpdir.join("empty_file.txt")
        test_data = ""

        FileProcessor.write_to_file(str(file_path), test_data)
        content = FileProcessor.read_from_file(str(file_path))

        assert content == test_data

    def test_file_write_read_multiline(self, tmpdir):
        """Тест запису та читання багаторядкового тексту."""
        file_path = tmpdir.join("multiline_file.txt")
        test_data = "Рядок 1\nРядок 2\nРядок 3\n"

        FileProcessor.write_to_file(str(file_path), test_data)
        content = FileProcessor.read_from_file(str(file_path))

        assert content == test_data

    def test_file_write_read_large_data(self, tmpdir):
        """Тест  запису та  читання великих обсягів даних ."""
        file_path = tmpdir.join("large_file.txt")
        # Створюємо рядок розміром приблизно 1MB
        test_data = "A" * (1024 * 1024)

        FileProcessor.write_to_file(str(file_path), test_data)
        content = FileProcessor.read_from_file(str(file_path))

        assert content == test_data
        assert len(content) == 1024 * 1024

    def test_file_write_read_unicode(self, tmpdir):
        """Тест запису та читання Unicode символів."""
        file_path = tmpdir.join("unicode_file.txt")
        test_data = "Привіт, світ! 🌍 测试 こんにちは"

        FileProcessor.write_to_file(str(file_path), test_data)
        content = FileProcessor.read_from_file(str(file_path))

        assert content == test_data

    def test_read_nonexistent_file(self):
        """Тест читання неіснуючого файлу."""
        with pytest.raises(FileNotFoundError) as exc_info:
            FileProcessor.read_from_file("nonexistent_file.txt")

        assert "Файл не знайдено" in str(exc_info.value)

    def test_write_to_nested_directory(self, tmpdir):
        """Тест запису у вкладену директорію (яка не існує)."""
        nested_path = tmpdir.join("nested", "deep", "testfile.txt")
        test_data = "Nested file content"

        FileProcessor.write_to_file(str(nested_path), test_data)
        content = FileProcessor.read_from_file(str(nested_path))

        assert content == test_data

    def test_append_to_file(self, tmpdir):
        """Тест додавання даних до файлу."""
        file_path = tmpdir.join("append_file.txt")
        initial_data = "Initial content\n"
        append_data = "Appended content"

        FileProcessor.write_to_file(str(file_path), initial_data)
        FileProcessor.append_to_file(str(file_path), append_data)
        content = FileProcessor.read_from_file(str(file_path))

        assert content == initial_data + append_data

    def test_file_exists(self, tmpdir):
        """Тест перевірки існування файлу."""
        existing_file = tmpdir.join("existing_file.txt")
        FileProcessor.write_to_file(str(existing_file), "test")

        assert FileProcessor.file_exists(str(existing_file)) is True
        assert FileProcessor.file_exists("nonexistent_file.txt") is False

    def test_overwrite_existing_file(self, tmpdir):
        """Тест  перезапису  існуючого  файлу ."""
        file_path = tmpdir.join("overwrite_file.txt")
        original_data = "Original content"
        new_data = "New content"

        FileProcessor.write_to_file(str(file_path), original_data)
        FileProcessor.write_to_file(str(file_path), new_data)
        content = FileProcessor.read_from_file(str(file_path))

        assert content == new_data

    @pytest.mark.parametrize("test_data", [
        "Simple text",
        "",
        "Text with\nnewlines\n",
        "Special chars: !@#$%^&*()",
        "Numbers: 1234567890",
        "Unicode: 你好世界"
    ])
    def test_write_read_parametrized(self, tmpdir, test_data):
        """Параметризований тест для різних типів даних."""
        file_path = tmpdir.join(f"param_test_{hash(test_data)}.txt")

        FileProcessor.write_to_file(str(file_path), test_data)
        content = FileProcessor.read_from_file(str(file_path))

        assert content == test_data


# Фікстури для складніших тестів
@pytest.fixture
def temp_file_with_content():
    """
    Фікстура для створення тимчасового файлу з контентом.

    Yields:
        tuple: (file_path, content)
    """
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        content = "Test content from fixture"
        f.write(content)
        temp_path = f.name

    try:
        yield temp_path, content
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


@pytest.fixture
def large_test_data():
    """Фікстура для створення великих тестових даних."""
    return ("Line {}\n".format(i) for i in range(10000))


class TestFileProcessorWithFixtures:
    """Додаткові тести з використанням користувацьких фікстур."""

    def test_read_existing_temp_file(self, temp_file_with_content):
        """Тест читання існуючого тимчасового файлу."""
        file_path, expected_content = temp_file_with_content
        content = FileProcessor.read_from_file(file_path)
        assert content == expected_content

    def test_large_data_processing(self, tmpdir, large_test_data):
        """Тест обробки великих даних з фікстурою."""
        file_path = tmpdir.join("large_data_test.txt")
        test_content = "".join(large_test_data)

        FileProcessor.write_to_file(str(file_path), test_content)
        content = FileProcessor.read_from_file(str(file_path))

        assert content == test_content
        assert content.count('\n') == 10000
