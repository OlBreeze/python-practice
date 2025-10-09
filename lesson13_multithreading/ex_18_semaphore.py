def worker(n):
    with semaphore:
        print(f"worker {n} start")
        time.sleep(1)
        print(f"worker {n} end")

# Необхідні імпорти
import threading
import time

# Створюємо семафор, який дозволяє одночасно працювати лише 2 потокам
semaphore = threading.Semaphore(2)

# Створюємо 5 потоків, кожен з яких буде виконувати функцію worker
threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]

# Запускаємо всі потоки
for t in threads:
    t.start()

# Чекаємо завершення всіх потоків
for t in threads:
    t.join()

#
# Цей код реалізує механізм обмеження ресурсів у багатопотоковому середовищі:
# threading.Semaphore(2): Створює "лічильник" із початковим значенням 2.
# with semaphore:: Кожен потік, перш ніж увійти в цей блок, намагається отримати "дозвіл" від семафора.
# Оскільки лічильник дорівнює 2, одночасно можуть виконуватися лише два потоки (worker 0 та worker 1).
# Інші потоки (3, 4, 5) будуть чекати на цьому рядку, поки один із активних потоків не завершиться і не звільнить дозвіл.