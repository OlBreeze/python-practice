import requests

def fetch_data(url: str) -> dict:
    """
    Делает GET-запрос к API и возвращает JSON-ответ.
    """
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()













# _______________________________________________________________________
# def test_fetch_data_success(requests_mock):
#     url = "https://olbreeze.github.io/weather"
#     mock_data = {"data": 42}
#
#     requests_mock.get(url, json=mock_data, status_code=200)
#
#     result = fetch_data(url)
#     assert result == mock_data
#
# def test_fetch_data_error(requests_mock):
#     url = "https://olbreeze.github.io/weather"
#
#     # имитируем ошибку 404
#     requests_mock.get(url, status_code=404)
#
#     with pytest.raises(requests.exceptions.HTTPError):
#         fetch_data(url)
