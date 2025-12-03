# Лекція: Інтеграція зовнішніх API

## 1. Вступ до API та їх типи

### Що таке API?
**API (Application Programming Interface)** — це інтерфейс програмування додатків, який дозволяє різним програмам взаємодіяти між собою. API визначає набір правил і протоколів для обміну даними між системами.

**Аналогія:** API — це як меню в ресторані. Ви (клієнт) не заходите на кухню, а просто обираєте страву з меню, і кухня (сервер) готує її для вас.

### Типи API

#### REST (Representational State Transfer)
- Найпопулярніший тип API
- Використовує HTTP протокол
- Працює з ресурсами через URL
- Повертає дані у форматі JSON або XML
- Простий у використанні та масштабуванні

#### SOAP (Simple Object Access Protocol)
- Більш формальний протокол
- Використовує XML для обміну повідомленнями
- Має вбудовані стандарти безпеки
- Складніший, але надійніший для корпоративних систем

#### GraphQL
- Мова запитів для API
- Дозволяє клієнту запитувати тільки потрібні дані
- Одна точка входу для всіх запитів
- Розроблений Facebook

### Роль API в інтеграції систем

API дозволяє:
- Об'єднувати різні сервіси в єдину систему
- Автоматизувати обмін даними
- Розділяти відповідальність між компонентами
- Створювати модульні та масштабовані рішення

### Приклади використання API

**Соціальні мережі:** Facebook API, Twitter API для авторизації, публікації контенту, отримання даних користувачів.

**Карти:** Google Maps API для відображення карт, побудови маршрутів, геокодування адрес.

**Платіжні системи:** Stripe API, PayPal API для обробки платежів, управління підписками.

---

## 2. Основи REST API

### Принципи REST

REST базується на концепції **CRUD** (Create, Read, Update, Delete) — чотирьох базових операціях з даними:

- **Create** — створення нового ресурсу
- **Read** — читання/отримання ресурсу
- **Update** — оновлення існуючого ресурсу
- **Delete** — видалення ресурсу

### HTTP методи

#### GET — отримання даних
```
GET /api/users
GET /api/users/123
```
- Отримує дані без їх зміни
- Може мати параметри запиту
- Безпечний метод (не змінює стан сервера)

#### POST — створення даних
```
POST /api/users
Body: {"name": "Іван", "email": "ivan@example.com"}
```
- Створює новий ресурс
- Дані передаються в тілі запиту
- Не ідемпотентний (повторний виклик створить новий ресурс)

#### PUT — повне оновлення
```
PUT /api/users/123
Body: {"name": "Іван Петров", "email": "ivan@example.com"}
```
- Оновлює всі поля ресурсу
- Ідемпотентний (повторний виклик дає той самий результат)

#### PATCH — часткове оновлення
```
PATCH /api/users/123
Body: {"email": "newemail@example.com"}
```
- Оновлює тільки вказані поля
- Більш ефективний для часткових змін

#### DELETE — видалення
```
DELETE /api/users/123
```
- Видаляє ресурс
- Ідемпотентний

### HTTP статуси відповідей

#### 2xx — Успішні відповіді
- **200 OK** — запит виконано успішно
- **201 Created** — ресурс створено
- **204 No Content** — успішно, але без даних у відповіді

#### 4xx — Помилки клієнта
- **400 Bad Request** — некоректний запит
- **401 Unauthorized** — потрібна авторизація
- **403 Forbidden** — доступ заборонено
- **404 Not Found** — ресурс не знайдено
- **429 Too Many Requests** — перевищено ліміт запитів

#### 5xx — Помилки сервера
- **500 Internal Server Error** — внутрішня помилка сервера
- **502 Bad Gateway** — помилка шлюзу
- **503 Service Unavailable** — сервіс недоступний

### Формати даних

#### JSON (JavaScript Object Notation)
```json
{
  "id": 123,
  "name": "Іван",
  "email": "ivan@example.com",
  "active": true,
  "roles": ["user", "admin"]
}
```
- Легкий і читабельний
- Стандарт для REST API
- Природна інтеграція з JavaScript

#### XML (eXtensible Markup Language)
```xml
<user>
  <id>123</id>
  <name>Іван</name>
  <email>ivan@example.com</email>
</user>
```
- Більш формальний
- Використовується в SOAP
- Підтримує схеми валідації

---

## 3. Робота з бібліотекою requests в Python

### Встановлення
```bash
pip install requests
```

### Базові операції

#### GET запит
```python
import requests

# Простий GET запит
response = requests.get('https://api.example.com/users')
print(response.status_code)  # 200
print(response.json())  # Парсить JSON відповідь

# GET з параметрами
params = {'city': 'Kyiv', 'limit': 10}
response = requests.get('https://api.example.com/data', params=params)
```

#### POST запит
```python
# Відправка JSON даних
data = {
    'name': 'Іван',
    'email': 'ivan@example.com'
}
response = requests.post('https://api.example.com/users', json=data)
print(response.json())
```

#### PUT/PATCH запит
```python
# Оновлення ресурсу
data = {'email': 'newemail@example.com'}
response = requests.patch('https://api.example.com/users/123', json=data)
```

#### DELETE запит
```python
response = requests.delete('https://api.example.com/users/123')
if response.status_code == 204:
    print("Користувача видалено")
```

### Обробка помилок
```python
try:
    response = requests.get('https://api.example.com/data', timeout=5)
    response.raise_for_status()  # Викличе помилку для 4xx/5xx
    data = response.json()
except requests.exceptions.Timeout:
    print("Час очікування вичерпано")
except requests.exceptions.HTTPError as e:
    print(f"HTTP помилка: {e}")
except requests.exceptions.RequestException as e:
    print(f"Помилка запиту: {e}")
```

---

## 4. Аутентифікація API

### Типи аутентифікації

#### API Key
Найпростіший спосіб — передача ключа в заголовках або параметрах:
```python
headers = {'X-API-Key': 'your_api_key_here'}
response = requests.get('https://api.example.com/data', headers=headers)

# Або в параметрах
params = {'api_key': 'your_api_key_here'}
response = requests.get('https://api.example.com/data', params=params)
```

#### Bearer Token (JWT)
```python
token = 'your_jwt_token_here'
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('https://api.example.com/protected', headers=headers)
```

#### Basic Authentication
```python
from requests.auth import HTTPBasicAuth

response = requests.get(
    'https://api.example.com/data',
    auth=HTTPBasicAuth('username', 'password')
)

# Скорочений варіант
response = requests.get('https://api.example.com/data', auth=('username', 'password'))
```

#### OAuth 2.0
Складніший протокол для безпечної авторизації:
```python
# Спрощений приклад
token_url = 'https://oauth.example.com/token'
data = {
    'grant_type': 'client_credentials',
    'client_id': 'your_client_id',
    'client_secret': 'your_client_secret'
}
token_response = requests.post(token_url, data=data)
access_token = token_response.json()['access_token']

# Використання токена
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.get('https://api.example.com/data', headers=headers)
```

---

## 5. Практичне завдання: Інтеграція з API погоди

### Опис завдання
Створити програму, яка використовує **OpenWeatherMap API** для отримання даних про погоду в обраному місті.

### Реєстрація та отримання API ключа

1. Зареєструйтесь на https://openweathermap.org/
2. Перейдіть в розділ API keys
3. Скопіюйте ваш API ключ

### Базова реалізація

```python
import requests

def get_weather(city, api_key):
    """
    Отримує дані про погоду для вказаного міста
    
    Args:
        city (str): Назва міста
        api_key (str): API ключ OpenWeatherMap
    
    Returns:
        dict: Дані про погоду
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',  # Цельсії
        'lang': 'ua'  # Українська мова
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Помилка при отриманні даних: {e}")
        return None

def display_weather(weather_data):
    """
    Виводить дані про погоду в читабельному форматі
    
    Args:
        weather_data (dict): Дані про погоду з API
    """
    if not weather_data:
        print("Не вдалося отримати дані про погоду")
        return
    
    city = weather_data['name']
    country = weather_data['sys']['country']
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    humidity = weather_data['main']['humidity']
    description = weather_data['weather'][0]['description']
    wind_speed = weather_data['wind']['speed']
    
    print(f"\n{'='*50}")
    print(f"Погода в місті {city}, {country}")
    print(f"{'='*50}")
    print(f"Температура: {temp}°C (відчувається як {feels_like}°C)")
    print(f"Опис: {description.capitalize()}")
    print(f"Вологість: {humidity}%")
    print(f"Швидкість вітру: {wind_speed} м/с")
    print(f"{'='*50}\n")

# Головна програма
if __name__ == "__main__":
    API_KEY = "your_api_key_here"  # Замініть на ваш ключ
    
    city = input("Введіть назву міста: ")
    weather_data = get_weather(city, API_KEY)
    display_weather(weather_data)
```

### Розширена версія з додатковими функціями

```python
import requests
from datetime import datetime

class WeatherAPI:
    """Клас для роботи з OpenWeatherMap API"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, city, units='metric', lang='ua'):
        """Отримує поточну погоду"""
        endpoint = f"{self.base_url}/weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': units,
            'lang': lang
        }
        return self._make_request(endpoint, params)
    
    def get_forecast(self, city, units='metric', lang='ua'):
        """Отримує прогноз на 5 днів"""
        endpoint = f"{self.base_url}/forecast"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': units,
            'lang': lang
        }
        return self._make_request(endpoint, params)
    
    def _make_request(self, endpoint, params):
        """Виконує HTTP запит"""
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                print("Місто не знайдено")
            elif response.status_code == 401:
                print("Невірний API ключ")
            else:
                print(f"HTTP помилка: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Помилка запиту: {e}")
            return None

def display_current_weather(data):
    """Виводить поточну погоду"""
    if not data:
        return
    
    print(f"\n{'='*60}")
    print(f"Поточна погода в місті {data['name']}, {data['sys']['country']}")
    print(f"{'='*60}")
    print(f"Температура: {data['main']['temp']:.1f}°C")
    print(f"Відчувається як: {data['main']['feels_like']:.1f}°C")
    print(f"Мін/Макс: {data['main']['temp_min']:.1f}°C / {data['main']['temp_max']:.1f}°C")
    print(f"Опис: {data['weather'][0]['description'].capitalize()}")
    print(f"Вологість: {data['main']['humidity']}%")
    print(f"Тиск: {data['main']['pressure']} гПа")
    print(f"Вітер: {data['wind']['speed']} м/с")
    print(f"Хмарність: {data['clouds']['all']}%")
    
    # Час сходу та заходу сонця
    sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
    sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
    print(f"Схід сонця: {sunrise}")
    print(f"Захід сонця: {sunset}")
    print(f"{'='*60}\n")

def display_forecast(data):
    """Виводить прогноз погоди"""
    if not data:
        return
    
    print(f"\n{'='*60}")
    print(f"Прогноз погоди для {data['city']['name']}, {data['city']['country']}")
    print(f"{'='*60}\n")
    
    for item in data['list'][:8]:  # Перші 24 години (кожні 3 години)
        dt = datetime.fromtimestamp(item['dt'])
        temp = item['main']['temp']
        description = item['weather'][0]['description']
        print(f"{dt.strftime('%d.%m %H:%M')} | {temp:.1f}°C | {description.capitalize()}")
    
    print(f"\n{'='*60}\n")

# Головна програма
def main():
    API_KEY = "your_api_key_here"  # Замініть на ваш ключ
    weather_api = WeatherAPI(API_KEY)
    
    while True:
        print("\nВиберіть опцію:")
        print("1. Поточна погода")
        print("2. Прогноз на 24 години")
        print("3. Вихід")
        
        choice = input("\nВаш вибір: ")
        
        if choice == '1':
            city = input("Введіть назву міста: ")
            data = weather_api.get_current_weather(city)
            display_current_weather(data)
        elif choice == '2':
            city = input("Введіть назву міста: ")
            data = weather_api.get_forecast(city)
            display_forecast(data)
        elif choice == '3':
            print("До побачення!")
            break
        else:
            print("Невірний вибір")

if __name__ == "__main__":
    main()
```

### Практичні завдання для самостійної роботи

1. **Додайте кешування:** Зберігайте отримані дані у файл і використовуйте їх, якщо запит повторюється протягом години.

2. **Порівняння міст:** Реалізуйте функцію порівняння погоди в кількох містах одночасно.

3. **Сповіщення:** Додайте функцію, яка сповіщає, якщо температура нижча або вища за вказаний поріг.

4. **Візуалізація:** Використайте бібліотеку matplotlib для побудови графіка температури на основі прогнозу.

5. **Telegram бот:** Створіть Telegram бота, який надсилає погоду за запитом користувача.

---

## Підсумок

На цій лекції ми розглянули основні концепції роботи з API, зокрема REST API, HTTP методи та статуси, аутентифікацію та практичну роботу з бібліотекою requests в Python. Практичне завдання з OpenWeatherMap API демонструє реальний приклад інтеграції зовнішнього сервісу в ваш додаток.

**Ключові моменти:**
- API — це стандартизований спосіб взаємодії між системами
- REST API використовує HTTP методи для операцій CRUD
- Правильна обробка помилок критично важлива при роботі з API
- Аутентифікація забезпечує безпеку доступу до даних
- Бібліотека requests робить роботу з API простою та зручною