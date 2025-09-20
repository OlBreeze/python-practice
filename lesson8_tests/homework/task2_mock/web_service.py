# web_service.py

import requests
from typing import Dict


class WebService:
    """
    Клас для отримання даних з веб-сайту через HTTP GET-запити.
    """

    def get_data(self, url: str) -> Dict:
        """
        Виконує GET-запит до заданого URL і повертає JSON-відповідь.

        Args:
            url (str): Адреса для запиту.

        Returns:
            dict: JSON-відповідь від сервера.

        Raises:
            requests.exceptions.HTTPError: якщо статус-код не 200.
        """
        response = requests.get(url)
        response.raise_for_status()  # Підніме помилку, якщо не 200
        return response.json()
