**Celery** — это распределённая очередь задач (task queue), написанная на Python. 
Она позволяет выполнять фоновые задачи асинхронно, планировать их выполнение, распределять нагрузку между несколькими воркерами и обеспечивать надёжную обработку задач.

Проще говоря: **Celery берёт задачу → отправляет в очередь → работники (workers) забирают и выполняют её → возвращают результат**.

---

# 🟩 **Зачем нужен Celery**

Celery используют, когда нужно:

* выполнять долгие операции вне основного веб-приложения
  *(например, отправка email, генерация отчёта, обработка изображений)*
* запускать задачи по расписанию
* обрабатывать много задач параллельно
* распределять нагрузку между серверами

---

# 🟩 **Как устроен Celery**

Celery состоит из трёх основных компонентов:

## 1. **Broker (брокер сообщений)**

Передаёт задачи от приложения к воркерам.
Обычно используют:

* Redis
* RabbitMQ

Брокер хранит очередь задач.

## 2. **Workers (воркеры)**

Процессы, которые выполняют задачи.
Они забирают задачи из брокера и запускают их.

## 3. **Backend (хранилище результатов)**

Сохраняет результаты выполнения задач.
Может быть:

* Redis
* SQL база
* RabbitMQ
* Memcached

---

# 🟩 **Как Celery работает — по шагам**

1. Ваше приложение (например, Django/Flask) отправляет задачу:

   ```python
   my_task.delay(10)
   ```
2. Celery отправляет эту задачу в брокер (например, Redis).
3. Один из воркеров получает задачу из очереди.
4. Выполняет её в отдельном процессе.
5. Результат отправляется в backend.
6. Приложение может получить результат через `AsyncResult`.

---

# 🟩 Пример кода (минимальный)

## 📌 **celery\_app.py**

```python
from celery import Celery

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)
```

## 📌 **tasks.py**

```python
from celery_app import app
import time

@app.task
def add(x, y):
    time.sleep(5)
    return x + y
```

## 📌 Запуск воркера

```bash
celery -A celery_app worker --loglevel=info
```

## 📌 Запуск задачи

```python
from tasks import add

result = add.delay(4, 6)
print(result.get())   # вернёт 10 через ~5 секунд
```

---

# 🟩 Плюсы Celery

* высокая производительность
* горизонтальное масштабирование
* поддержка планировщика (Celery Beat)
* надежная обработка задач
* большое комьюнити

# 🟥 Минусы

* сложность настройки
* требует внешних сервисов (Redis/RabbitMQ)
* не лучший выбор для очень тяжёлых вычислений (лучше использовать очереди + worker на Go/Node/C++)

---

# CELERY in my Project
У вас есть **код Celery** в артефактах, но **не настроено**. Давайте быстро реализуем:

## 🔧 Настройка Celery (шаг за шагом):

### 1. Установите зависимости:
```bash
pip install celery redis
```

### 2. Создайте `myproject/celery.py`:
```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

### 3. Измените `myproject/__init__.py`:
```python
from .celery import app as celery_app

__all__ = ('celery_app',)
```

### 4. Добавьте в `myproject/settings.py`:
```python
# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Kiev'

# Email (для тестування - вывод в консоль)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### 5. Создайте `myapp/tasks.py`:
```python
from celery import shared_task
from django.core.mail import send_mail
from .models import Book, Author
import csv
import time

@shared_task(bind=True)
def import_books_from_csv(self, file_path):
    try:
        total = 0
        imported = 0
        
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            total = len(rows)
            
            for i, row in enumerate(rows):
                self.update_state(
                    state='PROGRESS',
                    meta={'current': i + 1, 'total': total, 'percent': int((i + 1) / total * 100)}
                )
                
                author, _ = Author.objects.get_or_create(name=row['author'])
                Book.objects.create(
                    title=row['title'],
                    author=author,
                    published_year=int(row['year'])
                )
                
                imported += 1
                time.sleep(0.1)
        
        # Email
        send_mail(
            'Імпорт завершено',
            f'Успішно імпортовано {imported} книг з {total}',
            'from@example.com',
            ['to@example.com'],
        )
        
        return {'status': 'completed', 'imported': imported, 'total': total}
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
```

### 6. Добавьте views в `myapp/views.py`:
```python
from .tasks import import_books_from_csv
from celery.result import AsyncResult
from django.http import JsonResponse

def start_import(request):
    if request.method == 'POST':
        file_path = 'data/books.csv'  # Путь к CSV
        task = import_books_from_csv.delay(file_path)
        return JsonResponse({'task_id': task.id})
    
    return render(request, 'import_books.html')

def task_status(request, task_id):
    task = AsyncResult(task_id)
    
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Очікування...'}
    elif task.state == 'PROGRESS':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'percent': task.info.get('percent', 0),
        }
    elif task.state == 'SUCCESS':
        response = {'state': task.state, 'result': task.result}
    else:
        response = {'state': task.state, 'status': str(task.info)}
    
    return JsonResponse(response)
```

### 7. Добавьте URLs в `myapp/urls.py`:
```python
path('import/', views.start_import, name='import_books'),
path('task/<str:task_id>/', views.task_status, name='task_status'),
```

### 8. Создайте `data/books.csv`:
```csv
title,author,year
Кобзар,Тарас Шевченко,1840
Лісова пісня,Леся Українка,1911
Захар Беркут,Іван Франко,1883
```

### 9. Создайте шаблон `myapp/templates/import_books.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Імпорт книг</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; }
        button { padding: 10px 20px; background: #28a745; color: white; border: none; cursor: pointer; }
        #status { margin-top: 20px; padding: 15px; background: #f0f0f0; border-radius: 5px; }
        .progress { width: 100%; background: #ddd; height: 30px; border-radius: 5px; margin: 10px 0; }
        .progress-bar { height: 100%; background: #28a745; border-radius: 5px; transition: width 0.3s; }
    </style>
</head>
<body>
    <h2>Імпорт книг з CSV</h2>
    <button onclick="startImport()">Почати імпорт</button>
    <div id="status"></div>
    
    <script>
        function startImport() {
            fetch('/import/', {
                method: 'POST',
                headers: {'X-CSRFToken': '{{ csrf_token }}'}
            })
            .then(r => r.json())
            .then(data => {
                checkStatus(data.task_id);
            });
        }
        
        function checkStatus(taskId) {
            const interval = setInterval(() => {
                fetch(`/task/${taskId}/`)
                .then(r => r.json())
                .then(data => {
                    const status = document.getElementById('status');
                    
                    if (data.state === 'PROGRESS') {
                        status.innerHTML = `
                            <p>Прогрес: ${data.current} / ${data.total}</p>
                            <div class="progress">
                                <div class="progress-bar" style="width: ${data.percent}%">${data.percent}%</div>
                            </div>
                        `;
                    } else if (data.state === 'SUCCESS') {
                        status.innerHTML = `<p>✅ Завершено! Імпортовано: ${data.result.imported}</p>`;
                        clearInterval(interval);
                    } else {
                        status.innerHTML = `<p>Статус: ${data.status}</p>`;
                    }
                });
            }, 1000);
        }
    </script>
</body>
</html>
```

### 10. Запуск:

**Терминал 1 - Redis:**
```bash
redis-server
```

**Терминал 2 - Celery:**
```bash
celery -A myproject worker -l info
```

**Терминал 3 - Django:**
```bash
python manage.py runserver
```

### 11. Тестирование:
Откройте: `http://127.0.0.1:8000/import/`

---

**Хотите я создам все эти файлы в артефактах?** 🚀
