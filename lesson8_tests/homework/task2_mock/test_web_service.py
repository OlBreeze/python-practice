# Завдання 2. Мокування за допомогою unittest.mock
#
# Напишіть програму для отримання даних з веб-сайту та протестуйте його за допомогою моків.
# Напишіть клас WebService, який має метод get_data(url: str) -> dict.
# Цей метод повинен використовувати бібліотеку requests, щоб робити GET-запит та повертати JSON-відповідь.
# Використовуйте unittest.mock для макування HTTP-запитів.
# Замокуйте метод requests.get таким чином, щоб він повертав фейкову відповідь (наприклад, {"data": "test"}),
# та протестуйте метод get_data.
#
# Напишіть кілька тестів:
#
# перевірка успішного запиту (200),
# перевірка обробки помилки (404 чи інші коди).

# test_web_service.py

import unittest
from unittest.mock import patch, Mock
from web_service import WebService
import requests


class TestWebService(unittest.TestCase):
    def setUp(self):
        """
        Создание экземпляра WebService перед каждым тестом.
        """
        self.service = WebService()

    @patch('web_service.requests.get')
    def test_successful_get(self, mock_get):
        """
        Тест успішного отримання даних (200 OK).
        """
        # Створюємо відповідь
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_response.raise_for_status = Mock()  # нічого не робить
        mock_get.return_value = mock_response

        result = self.service.get_data("http://example.com")

        self.assertEqual(result, {"data": "test"})
        mock_get.assert_called_once_with("http://example.com")

    @patch('web_service.requests.get')
    def test_404_error(self, mock_get):
        """
        Тест обробки помилки 404.
        """
        # Створюємо відповідь з raise_for_status
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError):
            self.service.get_data("http://example.com/404")

        mock_get.assert_called_once_with("http://example.com/404")


if __name__ == "__main__":
    unittest.main()
