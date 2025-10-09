from multiprocessing import Process, Queue

def worker(q):
    q.put("Hello from process")

q = Queue()
p = Process(target=worker, args=(q,))
p.start()
p.join()
print(q.get())

#
# Queue() — это очередь, безопасная для обмена данными между процессами.
# Функция worker(q) кладёт в очередь строку "Hello from process".
# Process(target=worker, args=(q,)) запускает новый процесс, передавая ему очередь q.
#
# p.start() — запускает процесс.
# p.join() — ожидает завершения процесса.
# q.get() — получает сообщение из очереди и печатает его.