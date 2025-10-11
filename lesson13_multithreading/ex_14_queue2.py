import threading
import queue
import time


def producer(q):
    for i in range(5):
        time.sleep(1)
        q.put(i)
        print(f"Producer: Додав {i} у чергу")


def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break  # Завершення роботи
        print(f"Consumer: Отримав {item} з черги")
        q.task_done()


q = queue.Queue()

t1 = threading.Thread(target=producer, args=(q,))
t2 = threading.Thread(target=consumer, args=(q,), daemon=True)

t1.start()
t2.start()

t1.join()
q.put(None)  # Сигнал завершення
t2.join()

#
# Queue забезпечує безпечну передачу даних між потоками.
# q.put() додає елемент, а q.get() забирає.
# task_done() повідомляє, що елемент оброблено.
# daemon=True означає, що потік завершиться разом з головним потоком.