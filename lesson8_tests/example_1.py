import requests


# example_1.py - основные функции
def add(a, b):
    """Складывает два числа"""
    return a + b

def factorial(n):
    """Вычисляет факториал числа"""
    if n < 0:
        raise ValueError('n must be positive')
    else:
        return 1 if n == 0 else n * factorial(n - 1)

def divide(a, b):
    """Делит a на b"""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def is_even(n):
    """Проверяет, является ли число четным"""
    return n % 2 == 0

def get_user_info():
    """Возвращает информацию о пользователе"""
    return {
        'name': 'John',
        'age': 25,
        'email': 'john@example.com'
    }

def get_numbers():
    """Возвращает список чисел"""
    return [1, 2, 3, 4, 5]

def get_user(user_id):
    """Получает данные пользователя по ID"""
    response = requests.get(f'https://jsonplaceholder.typicode.com/users/{user_id}')
    response.raise_for_status()  # Поднять исключение если статус != 200
    return response.json()

def create_user(user_data):
    """Создает нового пользователя"""
    response = requests.post(
        'https://jsonplaceholder.typicode.com/users',
        json=user_data,
        headers={'Content-Type': 'application/json'}
    )
    response.raise_for_status()
    return response.json()

def update_user(user_id, user_data):
    """Обновляет данные пользователя"""
    response = requests.put(
        f'https://jsonplaceholder.typicode.com/users/{user_id}',
        json=user_data,
        headers={'Content-Type': 'application/json'}
    )
    response.raise_for_status()
    return response.json()

def delete_user(user_id):
    """Удаляет пользователя"""
    response = requests.delete(f'https://jsonplaceholder.typicode.com/users/{user_id}')
    response.raise_for_status()
    return response.status_code == 200

def get_users_list():
    """Получает список всех пользователей"""
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    response.raise_for_status()
    return response.json()

def get_user_posts(user_id):
    """Получает посты пользователя"""
    response = requests.get(f'https://jsonplaceholder.typicode.com/users/{user_id}/posts')
    response.raise_for_status()
    return response.json()

# Функция с обработкой ошибок
def get_user_safe(user_id):
    """Безопасное получение пользователя с обработкой ошибок"""
    try:
        response = requests.get(f'https://jsonplaceholder.typicode.com/users/{user_id}')
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None