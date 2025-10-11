import threading


def print_numbers():
    for i in range(5):
        print(i)


thread = threading.Thread(target=print_numbers)
thread.start()
thread.join()

# -----------------
counter = 0


def increment():
    global counter
    for _ in range(10000000):
        counter += 1


# Запуск потоків без синхронізації
thread1 = threading.Thread(target=increment)
thread2 = threading.Thread(target=increment)

thread1.start()
thread2.start()
thread1.join()
thread2.join()

print("Counter:", counter)  # Очікуване значення: 200000, але буде менше!