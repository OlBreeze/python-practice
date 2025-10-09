import threading

r_lock = threading.RLock()
counter = 0

def recursive_task(n):
    global counter
    if n <= 0:
        return

    # RLock дозволяє тому ж потоку повторно захоплювати блокування.
    with r_lock:
        counter += 1
        print(f'Recursive Task #{n}, counter: {counter}')
        recursive_task(n - 1)

# Створення та запуск потоку, який виконує рекурсивну функцію
t = threading.Thread(target=recursive_task, args=(5,))
t.start()

# Очікування завершення потоку
t.join()

print(f'finish value: {counter}')

#
# Цей код демонструє важливість використання threading.RLock (Reentrant Lock) у рекурсивних функціях:
#
# threading.RLock(): На відміну від звичайного Lock, RLock дозволяє потоку, який вже захопив блокування, викликати acquire() повторно без самоблокування.
# recursive_task: Кожен рекурсивний виклик функції знову входить у блок with r_lock:.
# Без RLock: Якби тут використовувався звичайний threading.Lock(),
# потік заблокувався б уже на першому рекурсивному виклику, оскільки спроба повторного захоплення призвела б до дедлоку.
# Результат: Лічильник (counter) коректно збільшиться 5 разів, і програма завершиться