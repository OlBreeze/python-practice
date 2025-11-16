
##    1. Управління сесіями та cookies 
    Login, Logout, Welcome
##    2.1. Оптимізація запитів у ORM 

-    Без оптимізації  - `Book.objects.all()` → много SQL запросов (N+1 проблема)
-    З оптимізацією  - `select_related('author').prefetch_related('reviews')` → 3 запроса вместо 50+
-    Вимірювання часу  - `time.time()` до и после, показывает разницу в секундах
-   Django Debug Toolbar показывает количество SQL запросов

---

##    2.2. Кешування 

 Где:  
- View: `books_list_cached` в `views.py`
- Settings: `CACHES` в `settings.py` (redis)

-   Кеширует список книг на 5 минут (`cache.set(cache_key, books, 300)`)
-   При обновлении страницы второй раз - данные из кеша (быстрее)
---

##    2.3. Django-debug-toolbar 

- Settings: `INSTALLED_APPS` и `MIDDLEWARE`
- Виден на всех страницах справа

---

##    2.4. Оптимізація шаблонів 

 Где:  `myapp/templates/books_list.html`, `statistics.html`

-   Шаблоны отображают книги с авторами и отзывами
-   Данные передаются оптимально (через `select_related`/`prefetch_related`)
-   Debug toolbar показывает что запросы оптимальны
---

##  2.5. Celery 

 Где:  
- `myproject/celery.py`, `myapp/tasks.py`
- View: `start_import`, `task_status`
- Шаблон: `import_books.html`

-   Импорт из CSV (`data/books.csv`)
-   Сохранение в БД
-   Email после завершения

---

##    3.1. Анотації та агрегації 

 Где:  `authors_statistics` в `views.py`

-   Средний рейтинг книг автора - `Avg('books__reviews__rating')`
-   Количество отзывов - `Count('books__reviews')`
-   Сортировка по рейтингу и отзывам - `order_by('-avg_rating', '-reviews_count')`
-   Отображение в таблице - `statistics.html`

---

##    3.2. Raw SQL 

 Где:  `authors_with_popular_books` в `views.py`

 Что делает: 
-   "Сирий" SQL запрос через `connection.cursor()`
-   Выбор авторов с книгами > 10 отзывов
-   Подсчет количества книг
-    Защита от SQL-инъекций  - использует параметризованные запросы 

---

##    3.3. Індексація 

 Где:  `myapp/models.py` - в `Meta` классах

 Что делает: 
-   Индексы на `Author.name`, `Book.title`, `Book.published_year`, `Review.rating`
-   Ускоряет поиск и сортировку


- Скриншоты в каталоге screens
- Рабочий код на GitHub
