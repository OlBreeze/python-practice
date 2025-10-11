Конечно! Вот пример **Race Condition** (состояние гонки) на Python:

---

## 🔴 Проблема: Race Condition

```python
import threading
import time

# Общая переменная (разделяемый ресурс)
balance = 1000

def withdraw(amount):
    """Снятие денег со счета"""
    global balance
    
    # Проверяем баланс
    if balance >= amount:
        print(f"Поток {threading.current_thread().name}: Проверка OK, баланс = {balance}")
        
        # Симуляция задержки (например, обращение к БД)
        time.sleep(0.1)
        
        # Снимаем деньги
        balance -= amount
        print(f"Поток {threading.current_thread().name}: Снято {amount}, остаток = {balance}")
    else:
        print(f"Поток {threading.current_thread().name}: Недостаточно средств")

# Создаём 2 потока, которые пытаются снять деньги одновременно
thread1 = threading.Thread(target=withdraw, args=(800,), name="Человек 1")
thread2 = threading.Thread(target=withdraw, args=(800,), name="Человек 2")

# Запускаем оба потока
thread1.start()
thread2.start()

# Ждём завершения
thread1.wait()
thread2.wait()

print(f"\nИтоговый баланс: {balance}")
```

---

## 🔥 Что произойдёт:

```
Поток Человек 1: Проверка OK, баланс = 1000
Поток Человек 2: Проверка OK, баланс = 1000
Поток Человек 1: Снято 800, остаток = 200
Поток Человек 2: Снято 800, остаток = -600

Итоговый баланс: -600
```

**Проблема:** Баланс стал **отрицательным (-600)**! Это недопустимо.

---

## 🤔 Почему так получилось?

1. **Поток 1** проверил баланс (1000 >= 800) ✅ → OK
2. **Поток 2** тоже проверил баланс (1000 >= 800) ✅ → OK
3. **Оба** считают что денег хватает
4. **Поток 1** снял 800 → баланс = 200
5. **Поток 2** снял 800 → баланс = -600 ❌

Это и есть **Race Condition** - результат зависит от того, кто "успел первым".

---

## ✅ Решение: Использовать Lock (мьютекс)

```python
import threading
import time

balance = 1000
lock = threading.Lock()  # Создаём "замок"

def withdraw_safe(amount):
    """Безопасное снятие денег"""
    global balance
    
    # БЛОКИРУЕМ доступ для других потоков
    with lock:
        # Теперь только ОДИН поток может быть здесь
        if balance >= amount:
            print(f"Поток {threading.current_thread().name}: Проверка OK, баланс = {balance}")
            time.sleep(0.1)  # Задержка
            balance -= amount
            print(f"Поток {threading.current_thread().name}: Снято {amount}, остаток = {balance}")
        else:
            print(f"Поток {threading.current_thread().name}: Недостаточно средств")
    # Замок автоматически снимается

# Создаём потоки
thread1 = threading.Thread(target=withdraw_safe, args=(800,), name="Человек 1")
thread2 = threading.Thread(target=withdraw_safe, args=(800,), name="Человек 2")

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print(f"\nИтоговый баланс: {balance}")
```

---

## ✅ Теперь результат правильный:

```
Поток Человек 1: Проверка OK, баланс = 1000
Поток Человек 1: Снято 800, остаток = 200
Поток Человек 2: Недостаточно средств

Итоговый баланс: 200
```

**Правильно!** Второй поток ждёт пока первый закончит, проверяет баланс (200) и видит что денег недостаточно.

---

## 🎯 Вывод:

**Race Condition** - когда несколько потоков одновременно изменяют общие данные, и результат зависит от порядка выполнения (случайности).

**Решение:**
- `threading.Lock()` - для синхронизации потоков
- `with lock:` - блокирует участок кода для одного потока

---

Понятно? 🚀