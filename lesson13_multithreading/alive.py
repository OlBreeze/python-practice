import threading
import time


def worker():
    print(f"Потік {threading.current_thread().name} почав роботу")
    time.sleep(2)
    print(f"Потік {threading.current_thread().name} завершив роботу")


# Створюємо потік
t = threading.Thread(target=worker, name="МійПотік")

print("Чи потік живий перед стартом?", t.is_alive())

t.start()

print("Назва потоку:", t.name)

t.name = "ОновленаНазва"
print("Оновлена назва потоку:", t.name)

time.sleep(1)
print("Чи потік живий під час роботи?", t.is_alive())

t.join()

print("Чи потік живий після завершення?", t.is_alive())