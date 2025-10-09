import threading
import time

# Створення обмеженого семафора, який дозволяє лише 2 потокам працювати одночасно
semaphore = threading.BoundedSemaphore(2)


def worker(n):
    print(f"Thread {n} is waiting...")
    semaphore.acquire()

    # Критична секція
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

# --- Демонстрація BoundedSemaphore ---

semaphore2 = threading.BoundedSemaphore(2)
semaphore2.acquire()
semaphore2.acquire()  # Лічильник тепер 0

semaphore2.release()  # Лічильник тепер 1
semaphore2.release()  # Лічильник тепер 2

# !!! Цей виклик призведе до помилки (ValueError), оскільки BoundedSemaphore
# не дозволяє лічильнику перевищити початкове значення (2).
semaphore2.release()

print('Counter more than start value!')
# Цей рядок не буде виконано, оскільки попередній виклик release() викличе ValueError.

#
# threading.BoundedSemaphore(N) працює так само, як і threading.Semaphore(N), але з однією важливою відмінністю:
# він викликає помилку ValueError, якщо ви намагаєтеся викликати release() більше разів, ніж було виконано acquire() (тобто, якщо лічильник перевищує початкове значення).
#
# Цей клас призначений для того, щоб уникнути програмних помилок, коли розробник помилково викликає release()
# занадто багато разів, що може приховати проблеми синхронізації.
#
# У наданому коді, останній виклик semaphore2.release() спричинить помилку, оскільки лічильник уже повернувся
# до початкового значення 2.