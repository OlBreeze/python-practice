import pytest
import requests
from unittest.mock import patch, Mock
from task8_fetch_data import fetch_data


def test_fetch_data_success():
    mock_response = Mock()
    mock_response.json.return_value = {"data": 42}
    mock_response.status_code = 200
    mock_response.raise_for_status = Mock()

    with patch("requests.get", return_value=mock_response) as mock_get:
        result = fetch_data("https://www.google.com/") # Внутри она вызовет requests.get(...), но этот вызов перехвачен patch и вместо реального интернета вернёт mock_response

        # проверяем вызов requests.get
        mock_get.assert_called_once_with("https://www.google.com/", timeout=5) # Проверка, что requests.get был вызван ровно один раз и именно с этими аргументами
        # проверяем, что функция вернула правильный JSON
        assert result == {"data": 42} # Проверяем, что функция вернула ожидаемый результат


def test_fetch_data_error():
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Not Found")
    mock_response.status_code = 404

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(requests.exceptions.HTTPError):
            fetch_data("https://www.google.com/")
