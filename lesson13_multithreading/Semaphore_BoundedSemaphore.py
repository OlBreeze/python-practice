import threading
import time

sem = threading.Semaphore(2)
bsem = threading.BoundedSemaphore(2)


def worker(sem_type, name):
    sem_type.acquire()
    print(f"{name} отримав доступ")
    time.sleep(1)
    sem_type.release()
    print(f"{name} звільнив доступ")


def incorrect_release():
    sem.release()  # ❌ Немає перевірки, можна викликати більше разів, ніж acquire
    print("Помилкове release() спрацювало")


def bounded_incorrect_release():
    try:
        bsem.release()  # ❌ Викличе помилку, якщо більше release, ніж acquire
    except ValueError as e:
        print("BoundedSemaphore: спроба зайвого release:", e)


# Перевірка Semaphore
threads = [threading.Thread(target=worker, args=(sem, f"Потік {i}")) for i in range(4)]
for t in threads: t.start()
for t in threads: t.join()

incorrect_release()  # Дозволено
bounded_incorrect_release()  # ValueError!
# ✅ Висновок:
#
# Semaphore дозволяє викликати release() більше, ніж acquire(), що може призвести до некоректної поведінки.
# BoundedSemaphore обмежує такі помилки, викликаючи ValueError.