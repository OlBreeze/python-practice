import threading

lock = threading.Lock()
rlock = threading.RLock()


def using_lock():
    lock.acquire()
    print("Lock отримано")
    lock.acquire()  # ❌ Deadlock! Потік сам себе блокує
    print("Цей рядок не виконається")
    lock.release()
    lock.release()


def using_rlock():
    rlock.acquire()
    print("RLock отримано")
    rlock.acquire()  # ✅ Без проблем, бо той самий потік
    print("Другий раз RLock отримано")
    rlock.release()
    rlock.release()


t1 = threading.Thread(target=using_rlock)
t1.start()
t1.join()

# ✅ Висновок:

# Lock підходить для звичайного використання між потоками.
# RLock варто застосовувати у випадках, коли один і той самий потік викликає заблоковані методи рекурсивно.