import threading
import time  # Необхідний для time.sleep

# Створення семафора, який дозволяє лише 2 потокам працювати одночасно
semaphore = threading.Semaphore(2)


def worker(n):
    # Потік чекає дозволу від семафора
    print(f"Thread {n} is waiting...")
    semaphore.acquire()

    # Критична секція: тут працюють лише 2 потоки
    print(f"Thread {n} is working...")
    time.sleep(1)

    # Потік звільняє дозвіл
    semaphore.release()
    print(f"Thread {n} is done...")


# Створення 5 потоків
threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]

# Запуск потоків
for t in threads:
    t.start()

# Очікування завершення всіх потоків
for t in threads:
    t.join()