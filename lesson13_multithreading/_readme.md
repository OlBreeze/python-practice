# Лекция: Параллельное программирование в Python

## 📚Основные разделы:

1. **Введение в параллельное программирование**
   - Процессы vs Потоки
   - Global Interpreter Lock (GIL)
   - Когда использовать что

2. **Многопоточность (Threading)**
   - Создание и управление потоками
   - Daemon-потоки
   - Проблема Race Condition
   - Механизмы синхронизации: Lock, RLock, Semaphore, Event, Condition, Barrier
   - Queue для обмена данными

3. **Многопроцессность (Multiprocessing)**
   - Создание процессов
   - Pool для эффективной обработки
   - Queue, Pipe для обмена данными
   - Value, Array, Manager для общих переменных

4. **concurrent.futures**
   - ThreadPoolExecutor и ProcessPoolExecutor
   - Обработка результатов и ошибок

5. **Проблемы параллельного программирования**
   - Race Condition
   - Deadlock (с решениями)
   - Starvation
   - Livelock

6. **Лучшие практики**
   - DO и DON'T
   - Паттерны: Producer-Consumer, Thread Pool, Reader-Writer

7. **Практические примеры**
   - Параллельная загрузка файлов
   - Обработка изображений
   - Веб-скрейпинг
   - Параллельные вычисления

8. **Профилирование и отладка**

💡 **Особенности лекции:**
- ✅ Готовые примеры кода
- ✅ Сравнительные таблицы
- ✅ Визуальные схемы
- ✅ Решения типичных проблем
- ✅ Практические задачи
- ✅ Лучшие практики

## 1. Введение в параллельное программирование

### 1.1 Основные концепции

#### Процесс (Process)
**Процесс** — это независимый экземпляр программы с собственным пространством памяти.

```
┌─────────────────┐
│    Процесс 1    │
│  ┌───────────┐  │
│  │  Память   │  │
│  │  Ресурсы  │  │
│  └───────────┘  │
└─────────────────┘

┌─────────────────┐
│    Процесс 2    │
│  ┌───────────┐  │
│  │  Память   │  │
│  │  Ресурсы  │  │
│  └───────────┘  │
└─────────────────┘
```

**Характеристики:**
- 🔒 Изолированная память
- 💪 Может использовать несколько ядер CPU
- 🐌 Высокие накладные расходы при создании
- 🔄 Сложный обмен данными

#### Поток (Thread)
**Поток** — это легковесная единица выполнения, которая работает в рамках одного процесса и использует общую память.

```
┌─────────────────────────┐
│        Процесс          │
│  ┌─────────────────┐    │
│  │  Общая память   │    │
│  └─────────────────┘    │
│    ↓     ↓     ↓        │
│  [T1]  [T2]  [T3]       │
│ Потоки                  │
└─────────────────────────┘
```

**Характеристики:**
- ✅ Общая память
- ⚡ Быстрое создание
- 🔄 Простой обмен данными
- ⚠️ Ограничение GIL в Python

### 1.2 Global Interpreter Lock (GIL)

**GIL** — это механизм в CPython, который позволяет выполнять только один поток Python-кода одновременно.

```python
# Псевдокод работы GIL
while True:
    поток = получить_следующий_поток()
    GIL.захватить()
    поток.выполнить_100_инструкций()
    GIL.освободить()
```

#### Почему GIL существует?
- 🛡️ Защита внутренних структур данных CPython
- 🎯 Упрощение управления памятью
- 🔒 Предотвращение состояния гонки

#### Влияние GIL

**I/O-bound задачи** (работа с файлами, сетью, БД):
- ✅ Многопоточность эффективна
- 🔓 GIL освобождается при ожидании I/O
- ⚡ Потоки могут работать параллельно

**CPU-bound задачи** (вычисления, обработка данных):
- ❌ Многопоточность неэффективна
- 🔒 GIL блокирует параллельное выполнение
- 🐌 Потоки выполняются последовательно

### 1.3 Когда использовать что?

| Тип задачи | Используйте | Причина |
|------------|-------------|---------|
| **I/O-bound** | `threading` | GIL освобождается при ожидании |
| **CPU-bound** | `multiprocessing` | Каждый процесс имеет свой GIL |
| **Смешанные** | `concurrent.futures` | Гибкость выбора |
| **Асинхронные** | `asyncio` | Эффективно для I/O |

---

## 2. Многопоточность (Threading)

### 2.1 Создание и запуск потоков

#### Базовый пример

```python
import threading
import time


def worker(name):
    """Функция, выполняемая в потоке"""
    print(f"Поток {name} начал работу")
    time.sleep(2)
    print(f"Поток {name} завершил работу")


# Создание потоков
thread1 = threading.Thread(target=worker, args=("A",), name="Thread-A")
thread2 = threading.Thread(target=worker, args=("B",), name="Thread-B")

# Запуск потоков
thread1.start()
thread2.start()

# Ожидание завершения
thread1.join()
thread2.join()

print("Главный поток завершён")
```

**Вывод:**
```
Поток A начал работу
Поток B начал работу
Поток A завершил работу
Поток B завершил работу
Главный поток завершён
```

#### Создание через класс

```python
import threading
import time


class MyThread(threading.Thread):
    def __init__(self, name, delay):
        super().__init__()
        self.name = name
        self.delay = delay

    def run(self):
        """Метод, который будет выполнен в потоке"""
        print(f"Поток {self.name} стартовал")
        for i in range(5):
            time.sleep(self.delay)
            print(f"Поток {self.name}: итерация {i}")
        print(f"Поток {self.name} завершён")


# Создание и запуск
t1 = MyThread("Alpha", 1)
t2 = MyThread("Beta", 2)

t1.start()
t2.start()

t1.join()
t2.join()

print("Все потоки завершены")
```

### 2.2 Управление потоками

#### Основные методы и атрибуты

```python
import threading
import time


def worker():
    time.sleep(2)
    print("Работа выполнена")


t = threading.Thread(target=worker, name="МойПоток")

# Информация о потоке
print(f"Имя потока: {t.name}")
print(f"Поток живой: {t.is_alive()}")  # False (не запущен)

t.start()

print(f"Поток живой: {t.is_alive()}")  # True (выполняется)
print(f"ID потока: {t.ident}")
print(f"Native ID: {t.native_id}")  # Python 3.8+

# Изменение имени
t.name = "ОбновлённоеИмя"
print(f"Новое имя: {t.name}")

t.join()

print(f"Поток живой: {t.is_alive()}")  # False (завершён)
```

#### Полезные функции модуля

```python
import threading

# Получить текущий поток
current = threading.current_thread()
print(f"Текущий поток: {current.name}")

# Список всех активных потоков
all_threads = threading.enumerate()
print(f"Активные потоки: {[t.name for t in all_threads]}")

# Количество активных потоков
count = threading.active_count()
print(f"Количество потоков: {count}")
```

#### Daemon-потоки

**Демон-поток** — фоновый поток, который автоматически завершается при завершении главного потока.

```python
import threading
import time


def daemon_worker():
    while True:
        print("Демон работает...")
        time.sleep(1)


def normal_worker():
    for i in range(3):
        print(f"Обычный поток: {i}")
        time.sleep(1)


# Демон-поток
daemon = threading.Thread(target=daemon_worker, daemon=True)
daemon.start()

# Обычный поток
normal = threading.Thread(target=normal_worker)
normal.start()

normal.join()
print("Главный поток завершён")
# Демон автоматически завершится
```

**Когда использовать daemon:**
- ✅ Фоновый мониторинг
- ✅ Логирование
- ✅ Сборка мусора
- ❌ Важные операции (могут прерваться)

### 2.3 Проблема состояния гонки (Race Condition)

#### Что это?

**Race Condition** возникает, когда несколько потоков одновременно изменяют общие данные.

```python
import threading

counter = 0


def increment():
    global counter
    for _ in range(100000):
        counter += 1  # ⚠️ НЕ АТОМАРНАЯ операция!


# Запуск без синхронизации
thread1 = threading.Thread(target=increment)
thread2 = threading.Thread(target=increment)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print(f"Counter: {counter}")
# Ожидаем: 200000
# Получаем: ~150000-190000 (зависит от запуска!)
```

#### Почему так происходит?

Операция `counter += 1` не атомарна:

```python
# Разложение на шаги:
# 1. temp = counter      # Чтение
# 2. temp = temp + 1     # Вычисление
# 3. counter = temp      # Запись

# Проблема при параллельном выполнении:
# Поток 1: читает 0
# Поток 2: читает 0
# Поток 1: записывает 1
# Поток 2: записывает 1
# Результат: 1 вместо 2!
```

### 2.4 Механизмы синхронизации

#### Lock (Блокировка)

**Lock** — простейший примитив синхронизации.

```python
import threading

counter = 0
lock = threading.Lock()


def increment():
    global counter
    for _ in range(100000):
        with lock:  # Автоматически acquire() и release()
            counter += 1


thread1 = threading.Thread(target=increment)
thread2 = threading.Thread(target=increment)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print(f"Counter: {counter}")  # Всегда 200000!
```

**Альтернативный синтаксис:**

```python
lock.acquire()
try:
    counter += 1
finally:
    lock.release()
```

#### Класс с Lock

```python
import threading


class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1

    def get_value(self):
        with self.lock:
            return self.value


counter = Counter()


def worker():
    for _ in range(100000):
        counter.increment()


threads = [threading.Thread(target=worker) for _ in range(5)]

for t in threads:
    t.start()

for t in threads:
    t.join()

print(f"Итоговое значение: {counter.get_value()}")  # 500000
```

#### RLock (Рекурсивная блокировка)

**RLock** позволяет одному потоку захватывать блокировку несколько раз.

```python
import threading

lock = threading.Lock()
rlock = threading.RLock()


def using_lock():
    """❌ Deadlock с обычным Lock"""
    lock.acquire()
    print("Lock получен")
    lock.acquire()  # Заблокируется навсегда!
    print("Этот код не выполнится")
    lock.release()
    lock.release()


def using_rlock():
    """✅ RLock позволяет повторный захват"""
    rlock.acquire()
    print("RLock получен первый раз")
    rlock.acquire()  # Без проблем!
    print("RLock получен второй раз")
    rlock.release()
    rlock.release()


t = threading.Thread(target=using_rlock)
t.start()
t.join()
```

**Когда использовать RLock:**
- ✅ Рекурсивные функции
- ✅ Вложенные вызовы методов
- ✅ Один поток берёт блокировку несколько раз

#### Semaphore (Семафор)

**Semaphore** ограничивает количество потоков, одновременно получающих доступ к ресурсу.

```python
import threading
import time

# Разрешить максимум 2 потока одновременно
semaphore = threading.Semaphore(2)


def worker(n):
    print(f"Поток {n} ожидает доступа...")
    with semaphore:
        print(f"✅ Поток {n} получил доступ")
        time.sleep(2)
        print(f"❌ Поток {n} освободил ресурс")


threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]

for t in threads:
    t.start()

for t in threads:
    t.join()
```

**Вывод:**
```
Поток 0 ожидает доступа...
Поток 1 ожидает доступа...
Поток 2 ожидает доступа...
✅ Поток 0 получил доступ
✅ Поток 1 получил доступ
# Остальные ждут...
```

**Применение:**
- 🗄️ Ограничение подключений к БД
- 📂 Ограничение доступа к файлам
- 🌐 Контроль количества запросов к API

#### BoundedSemaphore

**BoundedSemaphore** — безопасная версия Semaphore, предотвращающая ошибки при release().

```python
import threading

sem = threading.Semaphore(2)
bsem = threading.BoundedSemaphore(2)

# ❌ Semaphore: можно вызвать release() больше раз
sem.release()  # Работает, хотя acquire() не было
sem.release()  # Счётчик становится > 2

# ✅ BoundedSemaphore: защита от ошибок
try:
    bsem.release()  # ValueError!
except ValueError as e:
    print(f"Ошибка: {e}")
```

#### Event (Событие)

**Event** — сигнал для синхронизации потоков.

```python
import threading
import time

event = threading.Event()


def waiter(name):
    print(f"{name} ожидает сигнала...")
    event.wait()  # Ждёт, пока кто-то вызовет event.set()
    print(f"{name} получил сигнал!")


# Создание потоков
t1 = threading.Thread(target=waiter, args=("Поток-1",))
t2 = threading.Thread(target=waiter, args=("Поток-2",))

t1.start()
t2.start()

time.sleep(2)
print("Главный поток отправляет сигнал!")
event.set()  # Все ожидающие потоки продолжат работу

t1.join()
t2.join()
```

**Методы Event:**
- `set()` — установить сигнал (все потоки продолжают)
- `clear()` — сбросить сигнал
- `wait(timeout)` — ждать сигнала (с опциональным таймаутом)
- `is_set()` — проверить, установлен ли сигнал

#### Condition (Условие)

**Condition** — более гибкий механизм синхронизации.

```python
import threading
import time

condition = threading.Condition()
data = []


def producer():
    """Производитель данных"""
    for i in range(5):
        time.sleep(1)
        with condition:
            data.append(i)
            print(f"Произведено: {i}")
            condition.notify()  # Уведомить один ожидающий поток


def consumer():
    """Потребитель данных"""
    while True:
        with condition:
            while not data:
                condition.wait()  # Ждать данных
            item = data.pop(0)
            print(f"Потреблено: {item}")
            if item == 4:  # Последний элемент
                break


t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)

t1.start()
t2.start()

t1.join()
t2.join()
```

**Методы Condition:**
- `wait()` — ждать уведомления
- `notify(n=1)` — уведомить n потоков
- `notify_all()` — уведомить все ожидающие потоки

#### Barrier (Барьер)

**Barrier** — синхронизация группы потоков в одной точке.

```python
import threading
import time
import random

barrier = threading.Barrier(3)  # Ждёт 3 потока


def worker(n):
    print(f"Поток {n} начал работу")
    time.sleep(random.randint(1, 3))
    print(f"Поток {n} достиг барьера")
    
    barrier.wait()  # Ждёт, пока все 3 потока дойдут сюда
    
    print(f"Поток {n} продолжил работу")


threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]

for t in threads:
    t.start()

for t in threads:
    t.join()
```

**Применение:**
- 🏁 Синхронный старт потоков
- 🎯 Ожидание завершения фазы
- 🔄 Циклические алгоритмы

#### Timer (Таймер)

**Timer** — отложенный запуск функции.

```python
import threading


def hello():
    print("Привет через 3 секунды!")


timer = threading.Timer(3.0, hello)
timer.start()

print("Таймер запущен...")
# Через 3 секунды выполнится hello()

# Отменить таймер (если ещё не сработал)
# timer.cancel()
```

### 2.5 Обмен данными через Queue

**Queue** — потокобезопасная очередь для передачи данных.

```python
import threading
import queue
import time


def producer(q):
    """Производитель"""
    for i in range(5):
        time.sleep(1)
        q.put(i)
        print(f"Producer: добавил {i}")
    q.put(None)  # Сигнал завершения


def consumer(q):
    """Потребитель"""
    while True:
        item = q.get()
        if item is None:
            break
        print(f"Consumer: получил {i}")
        q.task_done()


q = queue.Queue()

t1 = threading.Thread(target=producer, args=(q,))
t2 = threading.Thread(target=consumer, args=(q,))

t1.start()
t2.start()

t1.join()
t2.join()
```

**Типы очередей:**

```python
import queue

# FIFO (First In First Out)
fifo = queue.Queue()

# LIFO (Last In First Out) - стек
lifo = queue.LifoQueue()

# Priority Queue (с приоритетами)
pq = queue.PriorityQueue()
pq.put((1, "важная задача"))
pq.put((5, "менее важная"))
pq.put((0, "срочная"))

while not pq.empty():
    print(pq.get())
```

---

## 3. Многопроцессность (Multiprocessing)

### 3.1 Создание и запуск процессов

#### Базовый пример

```python
import multiprocessing
import time


def worker(name):
    print(f"Процесс {name} запущен")
    time.sleep(2)
    print(f"Процесс {name} завершён")


if __name__ == "__main__":
    processes = []
    
    for i in range(3):
        p = multiprocessing.Process(target=worker, args=(f"Worker-{i}",))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print("Все процессы завершены")
```

**⚠️ Важно:** Код multiprocessing должен быть внутри `if __name__ == "__main__":`

### 3.2 Пул процессов (Pool)

**Pool** — удобный способ распределения задач между процессами.

```python
import multiprocessing


def square(x):
    return x * x


if __name__ == "__main__":
    # Создание пула из 4 процессов
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(square, range(10))
    
    print(results)
    # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

#### Методы Pool

```python
import multiprocessing
import time


def slow_square(x):
    time.sleep(1)
    return x * x


if __name__ == "__main__":
    with multiprocessing.Pool(4) as pool:
        # map() — синхронный
        result = pool.map(slow_square, [1, 2, 3, 4])
        print("map:", result)
        
        # map_async() — асинхронный
        async_result = pool.map_async(slow_square, [1, 2, 3, 4])
        print("Работа продолжается...")
        result = async_result.get()  # Ждём результата
        print("map_async:", result)
        
        # apply() — один аргумент, синхронно
        result = pool.apply(slow_square, (5,))
        print("apply:", result)
        
        # apply_async() — один аргумент, асинхронно
        async_result = pool.apply_async(slow_square, (6,))
        result = async_result.get()
        print("apply_async:", result)
```

### 3.3 Обмен данными между процессами

#### Queue

```python
import multiprocessing


def worker(q):
    q.put("Данные из подпроцесса")


if __name__ == "__main__":
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=worker, args=(q,))
    
    p.start()
    p.join()
    
    print(q.get())  # Получение данных
```

#### Pipe (Двусторонний канал)

```python
import multiprocessing


def worker(conn):
    conn.send("Привет от процесса!")
    response = conn.recv()
    print(f"Процесс получил: {response}")
    conn.close()


if __name__ == "__main__":
    parent_conn, child_conn = multiprocessing.Pipe()
    p = multiprocessing.Process(target=worker, args=(child_conn,))
    
    p.start()
    
    message = parent_conn.recv()
    print(f"Главный процесс получил: {message}")
    parent_conn.send("Ответ главного процесса")
    
    p.join()
```

### 3.4 Общие переменные

#### Value и Array

```python
import multiprocessing


def worker(val, arr):
    val.value += 1
    for i in range(len(arr)):
        arr[i] += 1


if __name__ == "__main__":
    # Общая переменная (целое число)
    val = multiprocessing.Value("i", 0)
    
    # Общий массив
    arr = multiprocessing.Array("i", [1, 2, 3, 4, 5])
    
    p1 = multiprocessing.Process(target=worker, args=(val, arr))
    p2 = multiprocessing.Process(target=worker, args=(val, arr))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    
    print(f"Value: {val.value}")
    print(f"Array: {list(arr)}")
```

**Типы для Value и Array:**
- `'i'` — целое число (int)
- `'f'` — float
- `'d'` — double
- `'c'` — char

#### Manager

**Manager** для сложных структур данных.

```python
import multiprocessing


def worker(shared_dict, shared_list):
    shared_dict["процесс"] = "изменил данные"
    shared_list.append("новый элемент")


if __name__ == "__main__":
    with multiprocessing.Manager() as manager:
        # Общий словарь
        shared_dict = manager.dict()
        shared_dict["ключ"] = "значение"
        
        # Общий список
        shared_list = manager.list([1, 2, 3])
        
        p = multiprocessing.Process(
            target=worker,
            args=(shared_dict, shared_list)
        )
        
        p.start()
        p.join()
        
        print(f"Словарь: {dict(shared_dict)}")
        print(f"Список: {list(shared_list)}")
```

### 3.5 Синхронизация процессов

```python
import multiprocessing
import time


def worker(lock, num):
    with lock:
        print(f"Процесс {num} получил блокировку")
        time.sleep(1)
        print(f"Процесс {num} освободил блокировку")


if __name__ == "__main__":
    lock = multiprocessing.Lock()
    
    processes = [
        multiprocessing.Process(target=worker, args=(lock, i))
        for i in range(3)
    ]
    
    for p in processes:
        p.start()
    
    for p in processes:
        p.join()
```

---

## 4. Модуль concurrent.futures

**concurrent.futures** — высокоуровневый интерфейс для работы с потоками и процессами.

### 4.1 ThreadPoolExecutor

```python
from concurrent.futures import ThreadPoolExecutor
import time


def task(n):
    print(f"Задача {n} начата")
    time.sleep(2)
    return n * n


# Использование пула потоков
with ThreadPoolExecutor(max_workers=3) as executor:
    # submit() — отправить одну задачу
    future = executor.submit(task, 5)
    print(f"Результат: {future.result()}")
    
    # map() — обработать список
    results = executor.map(task, range(5))
    print(f"Результаты: {list(results)}")
```

### 4.2 ProcessPoolExecutor

```python
from concurrent.futures import ProcessPoolExecutor


def compute(n):
    return sum(i * i for i in range(n))


if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = executor.map(compute, [10**6, 10**6, 10**6, 10**6])
        print(list(results))
```

### 4.3 Обработка результатов

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random


def task(n):
    delay = random.randint(1, 3)
    time.sleep(delay)
    return n, delay


with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(task, i) for i in range(5)]
    
    # Обработка по мере завершения
    for future in as_completed(futures):
        result, delay = future.result()
        print(f"Задача {result} завершена за {delay}с")
```

### 4.4 Обработка ошибок

```python
from concurrent.futures import ThreadPoolExecutor


def risky_task(n):
    if n == 3:
        raise ValueError("Ошибка в задаче 3!")
    return n * n


with ThreadPoolExecutor(max_workers=2) as executor:
    futures = [executor.submit(risky_task, i) for i in range(5)]
    
    for i, future in enumerate(futures):
        try:
            result = future.result()
            print(f"Задача {i}: {result}")
        except Exception as e:
            print(f"Задача {i}: ошибка — {e}")
```

---

## 5. Сравнение подходов

### Threading vs Multiprocessing vs concurrent.futures

| Критерий | Threading | Multiprocessing | concurrent.futures |
|----------|-----------|-----------------|-------------------|
| **Использование** | I/O-bound | CPU-bound | Универсально |
| **GIL** | Ограничивает | Обходит | Зависит от Executor |
| **Память** | Общая | Изолированная | Зависит от Executor |
| **Накладные расходы** | Низкие | Высокие | Средние |
| **Простота** | Средняя | Сложная | Простая |
| **Обмен данными** | Прямой | Через Queue/Pipe | Через futures |

### Когда что использовать?

```python
# ✅ I/O-bound: загрузка файлов, API запросы
from concurrent.futures import ThreadPoolExecutor

def download_file(url):
    # Имитация загрузки
    return url

with ThreadPoolExecutor(max_workers=10) as executor:
    urls = [f"http://example.com/file{i}" for i in range(10)]
    results = executor.map(download_file, urls)

# ✅ CPU-bound: вычисления, обработка данных
from concurrent.futures import ProcessPoolExecutor

def heavy_computation(n):
    return sum(i * i for i in range(n))

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = executor.map(heavy_computation, [10**6] * 10)

# ✅ Смешанные задачи
import concurrent.futures

def mixed_task(data):
    # CPU-bound часть
    result = heavy_computation(data)
    # I/O-bound часть
    save_to_file(result)
    return result