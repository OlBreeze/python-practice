# test_http_pytest.py - тесты HTTP запросов с pytest
import pytest
import requests
from unittest.mock import Mock, patch
from example_1 import get_user, create_user, get_users_list


# Фикстуры для тестовых данных
@pytest.fixture
def sample_user():
    """Фикстура с данными пользователя"""
    return {
        'id': 1,
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '1-770-736-8031 x56442'
    }


@pytest.fixture
def sample_users_list():
    """Фикстура со списком пользователей"""
    return [
        {'id': 1, 'name': 'User 1', 'email': 'user1@example.com'},
        {'id': 2, 'name': 'User 2', 'email': 'user2@example.com'},
        {'id': 3, 'name': 'User 3', 'email': 'user3@example.com'}
    ]


@pytest.fixture
def mock_response():
    """Фикстура для создания mock ответа"""

    def _mock_response(json_data, status_code=200):
        mock_resp = Mock()
        mock_resp.json.return_value = json_data
        mock_resp.status_code = status_code
        mock_resp.raise_for_status.return_value = None
        return mock_resp

    return _mock_response


# Простые тесты с pytest
@patch('example_1.requests.get')
def test_get_user_success(mock_get, sample_user, mock_response):
    """Тест успешного получения пользователя"""
    mock_get.return_value = mock_response(sample_user)

    user = get_user(1)

    assert user['id'] == 1
    assert user['name'] == 'John Doe'
    assert user['email'] == 'john@example.com'
    mock_get.assert_called_once_with('https://jsonplaceholder.typicode.com/users/1')


@patch('example_1.requests.get')
def test_get_user_not_found(mock_get):
    """Тест случая когда пользователь не найден"""
    mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("404")

    with pytest.raises(requests.exceptions.HTTPError):
        get_user(999)


@patch('example_1.requests.post')
def test_create_user_success(mock_post, mock_response):
    """Тест создания пользователя"""
    user_data = {'name': 'Jane Doe', 'email': 'jane@example.com'}
    created_user = {'id': 11, 'name': 'Jane Doe', 'email': 'jane@example.com'}

    mock_post.return_value = mock_response(created_user, 201)

    result = create_user(user_data)

    assert result['id'] == 11
    assert result['name'] == 'Jane Doe'
    mock_post.assert_called_once()


# Параметризованные тесты
@pytest.mark.parametrize("user_id,expected_name", [
    (1, "User 1"),
    (2, "User 2"),
    (3, "User 3"),
])
@patch('example_1.requests.get')
def test_get_user_parametrized(mock_get, mock_response, user_id, expected_name):
    """Параметризованный тест получения пользователей"""
    user_data = {'id': user_id, 'name': expected_name}
    mock_get.return_value = mock_response(user_data)

    user = get_user(user_id)

    assert user['id'] == user_id
    assert user['name'] == expected_name


# Тест с использованием фикстур
@patch('example_1.requests.get')
def test_get_users_list(mock_get, sample_users_list, mock_response):
    """Тест получения списка пользователей"""
    mock_get.return_value = mock_response(sample_users_list)

    users = get_users_list()

    assert len(users) == 3
    assert users[0]['name'] == 'User 1'
    assert all('email' in user for user in users)


# Тест с проверкой вызовов
@patch('example_1.requests.get')
def test_request_call_details(mock_get, sample_user, mock_response):
    """Детальная проверка параметров запроса"""
    mock_get.return_value = mock_response(sample_user)

    get_user(1)

    # Проверяем детали вызова
    assert mock_get.call_count == 1
    args, kwargs = mock_get.call_args
    assert args[0] == 'https://jsonplaceholder.typicode.com/users/1'


# Тест с множественными mock вызовами
@patch('example_1.requests')
def test_multiple_http_methods(mock_requests, mock_response):
    """Тест с несколькими HTTP методами"""
    # Настраиваем разные методы
    mock_requests.get.return_value = mock_response({'id': 1, 'name': 'John'})
    mock_requests.post.return_value = mock_response({'id': 2, 'name': 'Jane'}, 201)

    # Выполняем запросы
    user = get_user(1)
    created_user = create_user({'name': 'Jane'})

    assert user['name'] == 'John'
    assert created_user['name'] == 'Jane'

    # Проверяем вызовы
    mock_requests.get.assert_called_once()
    mock_requests.post.assert_called_once()


# Тест с обработкой исключений
@pytest.mark.parametrize("exception,expected_message", [
    (requests.exceptions.ConnectionError, "Connection error"),
    (requests.exceptions.Timeout, "Request timeout"),
    (requests.exceptions.HTTPError, "HTTP error"),
])
@patch('example_1.requests.get')
def test_request_exceptions(mock_get, exception, expected_message):
    """Тест различных исключений"""
    mock_get.side_effect = exception(expected_message)

    with pytest.raises(exception) as exc_info:
        get_user(1)

    assert expected_message in str(exc_info.value)


# Класс с тестами и setup
class TestHttpRequestsClass:
    """Класс тестов с setup методами"""

    def setup_method(self):
        """Выполняется перед каждым тестом"""
        self.base_url = "https://jsonplaceholder.typicode.com"
        self.sample_user = {'id': 1, 'name': 'Test User'}

    @patch('example_1.requests.get')
    def test_get_user_in_class(self, mock_get):
        """Тест внутри класса"""
        mock_resp = Mock()
        mock_resp.json.return_value = self.sample_user
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        user = get_user(1)
        assert user['name'] == 'Test User'


# Использование pytest-mock (более удобная альтернатива)
def test_with_mocker(mocker, sample_user):
    """Тест с использованием pytest-mock плагина"""
    # Требует установки: pip install pytest-mock
    mock_get = mocker.patch('example_1.requests.get')
    mock_response = Mock()
    mock_response.json.return_value = sample_user
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    user = get_user(1)
    assert user['name'] == 'John Doe'


# Использование responses (внешняя библиотека)
try:
    import responses


    @responses.activate
    def test_with_responses_library():
        """Тест с библиотекой responses"""
        # Регистрируем mock endpoint
        responses.add(
            responses.GET,
            'https://jsonplaceholder.typicode.com/users/1',
            json={'id': 1, 'name': 'Test User'},
            status=200
        )

        user = get_user(1)
        assert user['name'] == 'Test User'
        assert len(responses.calls) == 1


    @responses.activate
    def test_responses_with_error():
        """Тест ошибки с responses"""
        responses.add(
            responses.GET,
            'https://jsonplaceholder.typicode.com/users/999',
            json={'error': 'Not found'},
            status=404
        )

        # Нужно обработать в функции get_user
        # with pytest.raises(requests.exceptions.HTTPError):
        #     get_user(999)

except ImportError:
    # responses не установлен
    pass


# Интеграционные тесты (осторожно!)
@pytest.mark.integration
@pytest.mark.skip(reason="Реальный API - запускать только при необходимости")
def test_real_api_integration():
    """Реальный интеграционный тест"""
    try:
        user = get_user(1)
        assert isinstance(user, dict)
        assert 'id' in user
        assert 'name' in user
    except requests.exceptions.RequestException:
        pytest.skip("API недоступен")


# Тест производительности
@pytest.mark.slow
@patch('example_1.requests.get')
def test_performance_multiple_calls(mock_get, mock_response):
    """Тест производительности множественных вызовов"""
    mock_get.return_value = mock_response({'id': 1, 'name': 'User'})

    import time
    start_time = time.time()

    # Делаем много вызовов
    for i in range(100):
        get_user(1)

    end_time = time.time()
    duration = end_time - start_time

    assert duration < 1.0  # Должно выполниться быстро с mock
    assert mock_get.call_count == 100


# Конфигурация и маркеры
"""
# pytest.ini или setup.cfg

[tool:pytest]
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    http: marks tests that involve HTTP requests

# Команды для запуска:
pytest test_http_pytest.py                    # Все тесты
pytest -m "not slow"                         # Исключить медленные тесты  
pytest -m "unit"                             # Только unit тесты
pytest -k "get_user"                         # Тесты содержащие "get_user"
pytest --tb=short                           # Короткий traceback
pytest -v                                   # Подробный вывод
pytest --maxfail=1                          # Остановить после первой ошибки
"""


# Фикстуры уровня модуля/сессии
@pytest.fixture(scope="session")
def api_client():
    """Фикстура уровня сессии для API клиента"""
    # Настройка клиента один раз для всех тестов
    client_config = {
        'base_url': 'https://jsonplaceholder.typicode.com',
        'timeout': 30
    }
    yield client_config
    # Очистка после всех тестов
    print("Cleaning up API client")


@pytest.fixture(scope="module")
def database_setup():
    """Фикстура уровня модуля для настройки БД"""
    # Настройка БД для всех тестов модуля
    print("Setting up test database")
    yield "test_db_connection"
    print("Tearing down test database")


# Автоматические фикстуры
@pytest.fixture(autouse=True)
def setup_and_cleanup():
    """Автоматически выполняется для каждого теста"""
    print("Setup before test")
    yield
    print("Cleanup after test")


# Пример запуска тестов программно
if __name__ == "__main__":
    # Запуск с pytest
    pytest.main([__file__, "-v"])