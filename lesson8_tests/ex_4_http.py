# test_http_requests.py - тесты HTTP запросов
import unittest
from unittest.mock import patch, Mock, MagicMock
import requests
import json
from example_1 import (
    get_user, create_user, update_user, delete_user,
    get_users_list, get_user_posts, get_user_safe
)


class TestHttpRequests(unittest.TestCase):
    """Тесты HTTP запросов с использованием mock"""

    @patch('example_1.requests.get')
    def test_get_user_success(self, mock_get):
        """Тест успешного получения пользователя"""
        # Настраиваем mock ответ
        mock_response = Mock()
        mock_response.json.return_value = {
            'id': 1,
            'name': 'John Doe',
            'email': 'john@example.com'
        }
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Выполняем тест
        user = get_user(1)

        # Проверяем результат
        self.assertEqual(user['id'], 1)
        self.assertEqual(user['name'], 'John Doe')
        self.assertEqual(user['email'], 'john@example.com')

        # Проверяем, что requests.get был вызван правильно
        mock_get.assert_called_once_with('https://jsonplaceholder.typicode.com/users/1')

    @patch('example_1.requests.get')
    def test_get_user_not_found(self, mock_get):
        """Тест случая когда пользователь не найден"""
        # Настраиваем mock для 404 ошибки
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        # Проверяем, что поднимается исключение
        with self.assertRaises(requests.exceptions.HTTPError):
            get_user(999)

    @patch('example_1.requests.post')
    def test_create_user_success(self, mock_post):
        """Тест создания пользователя"""
        # Подготавливаем тестовые данные
        user_data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com'
        }

        # Настраиваем mock ответ
        mock_response = Mock()
        mock_response.json.return_value = {
            'id': 11,
            'name': 'Jane Doe',
            'email': 'jane@example.com'
        }
        mock_response.status_code = 201
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # Выполняем тест
        created_user = create_user(user_data)

        # Проверяем результат
        self.assertEqual(created_user['id'], 11)
        self.assertEqual(created_user['name'], 'Jane Doe')

        # Проверяем параметры вызова
        mock_post.assert_called_once_with(
            'https://jsonplaceholder.typicode.com/users',
            json=user_data,
            headers={'Content-Type': 'application/json'}
        )

    @patch('example_1.requests.put')
    def test_update_user_success(self, mock_put):
        """Тест обновления пользователя"""
        user_data = {'name': 'Updated Name'}

        mock_response = Mock()
        mock_response.json.return_value = {
            'id': 1,
            'name': 'Updated Name',
            'email': 'john@example.com'
        }
        mock_response.raise_for_status.return_value = None
        mock_put.return_value = mock_response

        result = update_user(1, user_data)

        self.assertEqual(result['name'], 'Updated Name')
        mock_put.assert_called_once_with(
            'https://jsonplaceholder.typicode.com/users/1',
            json=user_data,
            headers={'Content-Type': 'application/json'}
        )

    @patch('example_1.requests.delete')
    def test_delete_user_success(self, mock_delete):
        """Тест удаления пользователя"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_delete.return_value = mock_response

        result = delete_user(1)

        self.assertTrue(result)
        mock_delete.assert_called_once_with('https://jsonplaceholder.typicode.com/users/1')

    @patch('example_1.requests.get')
    def test_get_users_list_success(self, mock_get):
        """Тест получения списка пользователей"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {'id': 1, 'name': 'User 1'},
            {'id': 2, 'name': 'User 2'},
            {'id': 3, 'name': 'User 3'}
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        users = get_users_list()

        self.assertEqual(len(users), 3)
        self.assertEqual(users[0]['name'], 'User 1')
        mock_get.assert_called_once_with('https://jsonplaceholder.typicode.com/users')

    @patch('example_1.requests.get')
    def test_get_user_posts_success(self, mock_get):
        """Тест получения постов пользователя"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {'id': 1, 'title': 'Post 1', 'userId': 1},
            {'id': 2, 'title': 'Post 2', 'userId': 1}
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        posts = get_user_posts(1)

        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0]['title'], 'Post 1')
        mock_get.assert_called_once_with('https://jsonplaceholder.typicode.com/users/1/posts')

    @patch('example_1.requests.get')
    def test_get_user_safe_not_found(self, mock_get):
        """Тест безопасного получения несуществующего пользователя"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        user = get_user_safe(999)

        self.assertIsNone(user)

    @patch('example_1.requests.get')
    def test_get_user_safe_network_error(self, mock_get):
        """Тест обработки сетевой ошибки"""
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        user = get_user_safe(1)

        self.assertIsNone(user)

    # Тест с использованием context manager
    @patch('example_1.requests.get')
    def test_get_user_with_context_manager(self, mock_get):
        """Альтернативный способ патчинга с context manager"""
        mock_response = Mock()
        mock_response.json.return_value = {'id': 1, 'name': 'Test User'}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with patch('example_1.requests.get', return_value=mock_response) as mock:
            user = get_user(1)
            self.assertEqual(user['name'], 'Test User')
            mock.assert_called_once()


class TestHttpRequestsAdvanced(unittest.TestCase):
    """Продвинутые техники тестирования HTTP запросов"""

    def setUp(self):
        """Настройка для каждого теста"""
        self.sample_user = {
            'id': 1,
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '1-770-736-8031 x56442'
        }

    @patch('example_1.requests')
    def test_multiple_requests_calls(self, mock_requests):
        """Тест нескольких вызовов requests"""
        # Настраиваем разные ответы для разных методов
        mock_get_response = Mock()
        mock_get_response.json.return_value = self.sample_user
        mock_get_response.raise_for_status.return_value = None

        mock_post_response = Mock()
        mock_post_response.json.return_value = {'id': 2, 'name': 'Created User'}
        mock_post_response.status_code = 201
        mock_post_response.raise_for_status.return_value = None

        # Настраиваем методы
        mock_requests.get.return_value = mock_get_response
        mock_requests.post.return_value = mock_post_response

        # Выполняем тесты
        user = get_user(1)
        created_user = create_user({'name': 'New User'})

        self.assertEqual(user['name'], 'John Doe')
        self.assertEqual(created_user['name'], 'Created User')

    @patch('example_1.requests.get')
    def test_request_with_custom_assertions(self, mock_get):
        """Тест с детальными проверками запроса"""
        mock_response = Mock()
        mock_response.json.return_value = self.sample_user
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        get_user(1)

        # Детальные проверки
        self.assertEqual(mock_get.call_count, 1)
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], 'https://jsonplaceholder.typicode.com/users/1')

    @patch('example_1.requests.get')
    def test_response_properties(self, mock_get):
        """Тест проверки свойств ответа"""
        mock_response = Mock()
        mock_response.json.return_value = self.sample_user
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.url = 'https://jsonplaceholder.typicode.com/users/1'
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        get_user(1)

        # Можем проверить свойства mock объекта
        self.assertEqual(mock_response.status_code, 200)
        self.assertIn('application/json', mock_response.headers['Content-Type'])

    # Параметризованный тест для разных пользователей
    def test_get_multiple_users(self):
        """Тест получения разных пользователей"""
        test_cases = [
            (1, 'User 1'),
            (2, 'User 2'),
            (3, 'User 3')
        ]

        for user_id, expected_name in test_cases:
            with self.subTest(user_id=user_id):
                with patch('example_1.requests.get') as mock_get:
                    mock_response = Mock()
                    mock_response.json.return_value = {
                        'id': user_id,
                        'name': expected_name
                    }
                    mock_response.raise_for_status.return_value = None
                    mock_get.return_value = mock_response

                    user = get_user(user_id)
                    self.assertEqual(user['name'], expected_name)


class TestRealHttpRequests(unittest.TestCase):
    """Тесты реальных HTTP запросов (интеграционные тесты)"""

    @unittest.skip("Интеграционный тест - запускать только при необходимости")
    def test_real_api_call(self):
        """Реальный вызов API (осторожно с лимитами!)"""
        try:
            user = get_user(1)
            self.assertIsInstance(user, dict)
            self.assertIn('id', user)
            self.assertIn('name', user)
        except requests.exceptions.RequestException:
            self.skipTest("API недоступен")


# Пример использования responses библиотеки (альтернатива mock)
"""
# Установка: pip install responses

import responses
import requests

class TestWithResponses(unittest.TestCase):

    @responses.activate
    def test_get_user_with_responses(self):
        # Регистрируем mock ответ
        responses.add(
            responses.GET,
            'https://jsonplaceholder.typicode.com/users/1',
            json={'id': 1, 'name': 'Test User'},
            status=200
        )

        user = get_user(1)
        self.assertEqual(user['name'], 'Test User')

        # Проверяем что был сделан запрос
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, 
                        'https://jsonplaceholder.typicode.com/users/1')
"""

if __name__ == '__main__':
    # Запуск тестов с подробным выводом
    unittest.main(verbosity=2)

    # Альтернативные способы запуска:

    # 1. Запуск только mock тестов (быстрые)
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestHttpRequests)
    # unittest.TextTestRunner(verbosity=2).run(suite)

    # 2. Запуск с фильтрацией
    # python -m unittest test_http_requests.TestHttpRequests.test_get_user_success -v