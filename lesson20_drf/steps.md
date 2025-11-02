
# ============================================================
# ІНСТРУКЦІЇ ПО ЗАПУСКУ ПРОЄКТУ
# ============================================================
"""
1. Створіть віртуальне середовище:
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows

2. Встановіть залежності:
   pip install -r requirements.txt

---

3. Створіть базу даних і застосуйте міграції:
   python manage.py makemigrations
   python manage.py migrate

4. Створіть суперкористувача (адміністратора):
   python manage.py createsuperuser

5. Запустіть сервер:
   python manage.py runserver

6. Доступ до API:
   - Swagger документація: http://localhost:8000/docs/
   - ReDoc документація: http://localhost:8000/redoc/
   - Admin панель: http://localhost:8000/admin/

7. Запуск тестів:
   python manage.py test

   Запуск тестів з деталізацією:
   python manage.py test --verbosity=2

   Запуск тестів для конкретного додатку:
   python manage.py test books
   python manage.py test authentication

8. Приклади використання API:

   a) Реєстрація користувача:
   POST http://localhost:8000/api/auth/register/
   {
       "username": "johndoe",
       "email": "john@example.com",
       "password": "SecurePass123!",
       "password2": "SecurePass123!",
       "first_name": "John",
       "last_name": "Doe"
   }

   b) Отримання JWT токену:
   POST http://localhost:8000/api/auth/token/
   {
       "username": "johndoe",
       "password": "SecurePass123!"
   }

   c) Створення книги (потрібен токен):
   POST http://localhost:8000/api/books/
   Headers: Authorization: Bearer <your_access_token>
   {
       "title": "Кобзар",
       "author": "Тарас Шевченко",
       "genre": "Поезія",
       "publication_year": 1840
   }

   d) Отримання списку книг з фільтрацією:
   GET http://localhost:8000/api/books/?author=Шевченко&ordering=-publication_year
   Headers: Authorization: Bearer <your_access_token>

   e) Пошук книг:
   GET http://localhost:8000/api/books/?search=Кобзар
   Headers: Authorization: Bearer <your_access_token>

   f) Отримання статистики:
   GET http://localhost:8000/api/books/statistics/
   Headers: Authorization: Bearer <your_access_token>

   g) Отримання моїх книг:
   GET http://localhost:8000/api/books/my_books/
   Headers: Authorization: Bearer <your_access_token>

9. Структура ендпоінтів:

   АУТЕНТИФІКАЦІЯ:
   - POST   /api/auth/register/          - Реєстрація користувача
   - POST   /api/auth/token/             - Отримання JWT токену
   - POST   /api/auth/token/refresh/     - Оновлення JWT токену
   - GET    /api/auth/profile/           - Отримання профілю
   - PUT    /api/auth/profile/           - Оновлення профілю
   - PATCH  /api/auth/profile/           - Часткове оновлення профілю
   - POST   /api/auth/change-password/   - Зміна пароля

   КНИГИ:
   - GET    /api/books/                  - Список книг (з фільтрами)
   - POST   /api/books/                  - Створення книги
   - GET    /api/books/{id}/             - Деталі книги
   - PUT    /api/books/{id}/             - Оновлення книги
   - PATCH  /api/books/{id}/             - Часткове оновлення
   - DELETE /api/books/{id}/             - Видалення книги (тільки admin)
   - GET    /api/books/my_books/         - Мої книги
   - GET    /api/books/statistics/       - Статистика

10. Параметри фільтрації та пошуку:
    - author=<текст>              - Фільтр за автором
    - genre=<текст>               - Фільтр за жанром
    - publication_year=<рік>      - Фільтр за роком
    - year_from=<рік>             - Від року
    - year_to=<рік>               - До року
    - search=<текст>              - Пошук за назвою/автором
    - ordering=<поле>             - Сортування (title, author, publication_year, created_at)
                                    Для зворотного порядку: -<поле>
    - page=<номер>                - Номер сторінки (пагінація)

11. Особливості реалізації:
    - Окремий додаток authentication для всієї логіки аутентифікації
    - JWT токени з автоматичним оновленням
    - Дозволи на рівні ViewSet та об'єкта
    - Автоматична документація API через Swagger
    - Повне покриття тестами (15+ тестів)
    - Валідація даних на рівні серіалізаторів
    - Оптимізовані запити до БД (select_related)
    - Індекси для покращення продуктивності

12. Безпека:
    - Тільки автентифіковані користувачі мають доступ до API
    - Видалення книг дозволене тільки адміністраторам
    - Редагування книг дозволене тільки власнику або адміністратору
    - Пароль валідується Django password validators
    - JWT токени мають обмежений термін дії
    - CSRF захист включений

13. Розширення функціоналу:
    - Додано поле user до моделі Book
    - Реалізовано реєстрацію та управління профілем
    - Додано зміну пароля
    - Додано статистику по книгах
    - Додано ендпоінт "мої книги"
    - Сортування за різними полями
    
МІКРОСЕРВІСНА АРХІТЕКТУРА:
Так, authentication додаток можна легко перетворити на окремий мікросервіс:

1. Винесіть додаток authentication в окремий проєкт Django
2. Налаштуйте окрему базу даних для користувачів
3. Використовуйте спільну JWT SECRET_KEY для обох сервісів
4. Books сервіс буде валідувати токени від Authentication сервісу
5. Комунікація через REST API або gRPC

Переваги такого підходу:
- Незалежне масштабування сервісів
- Різні команди можуть працювати над різними сервісами
- Легше оновлювати та деплоїти окремі компоненти
- Можливість використання різних технологій для різних сервісів

В поточній реалізації authentication вже виділений в окремий додаток (app),
що є першим кроком до мікросервісної архітектури.
"""