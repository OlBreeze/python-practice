from concurrent.futures import ThreadPoolExecutor

def square(x):
    return x * x

with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(square, range(100))
    print(list(results))

#
# ThreadPoolExecutor создаёт пул потоков (в данном случае — 4 потока).
#
# Функция square(x) вычисляет квадрат числа.
#
# executor.map(square, range(100)) распределяет вычисления по потокам: каждый поток обрабатывает часть чисел.
#
# Результаты собираются в объект results, который превращается в список.