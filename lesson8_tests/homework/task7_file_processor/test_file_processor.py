"""
Тести для модуля file_processor.
"""

import pytest
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

    def test_read_nonexistent_file(self):
        """Тест читання неіснуючого файлу."""
        with pytest.raises(FileNotFoundError) as exc_info:
            FileProcessor.read_from_file("nonexistent_file.txt")

        assert "Файл не знайдено" in str(exc_info.value)

    def test_overwrite_existing_file(self, tmpdir):
        """Тест перезапису існуючого файлу."""
        file_path = tmpdir.join("overwrite_file.txt")
        original_data = "Original content"
        new_data = "New content"

        FileProcessor.write_to_file(str(file_path), original_data)
        FileProcessor.write_to_file(str(file_path), new_data)
        content = FileProcessor.read_from_file(str(file_path))

        assert content == new_data
