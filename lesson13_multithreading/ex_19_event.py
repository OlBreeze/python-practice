import threading
import time

event = threading.Event()

def worker():
    print("Waiting for event...")
    event.wait()
    print("Event received! Doing work...")

# Створюємо та запускаємо потік
t = threading.Thread(target=worker)
t.start()

time.sleep(3)
print("Work done!")
event.set()
# Чекаємо, доки потік t завершиться
t.join()

#
# event = threading.Event(): Створюється об'єкт події, який спочатку знаходиться у стані "не встановлено" (False).
#
# Потік t (worker):
# Запускається і виконує print("Waiting for event...").
# Досягає event.wait(), який блокує потік доти, доки подія не буде встановлена.
#
# Основний потік:
# Призупиняється на 3 секунди (time.sleep(3)).
# Друкує "Work done!".
# Викликає event.set(), що переводить подію у стан "встановлено" (True).
#
# Потік t (продовження):
# Після event.set(), event.wait() розблоковується.
# Потік друкує "Event received! Doing work...".
#
# Завершує виконання.
#
# t.join(): Основний потік чекає повного завершення потоку t.