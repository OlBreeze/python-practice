import threading

def increment():
    global counter
    for _ in range(100000):
        counter += 1

counter = 0
threads = [threading.Thread(target=increment) for _ in range(2)]

for t in threads:
    t.start()

for t in threads:
    t.join()

print(counter)
#Результат counter может быть меньше ожидаемого (200000), из-за гонки потоков (race condition).
# Чтобы исправить это, нужно использовать блокировку: