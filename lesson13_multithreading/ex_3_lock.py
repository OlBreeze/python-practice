import threading

def increment():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1

counter = 0
lock = threading.Lock() # lock = threading.RLock() - повторное освобожд ресурса, рекурсия
threads = [threading.Thread(target=increment) for _ in range(2)]

for t in threads:
    t.start()

for t in threads:
    t.join()

print(counter)
