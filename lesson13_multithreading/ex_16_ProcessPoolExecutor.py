from concurrent.futures import ProcessPoolExecutor

def cube(x):
    return x ** 3

with ProcessPoolExecutor(max_workers=4) as executor:
    results = executor.map(cube, range(100))
    print(list(results))

# Код використовує 4 процеси для паралельного обчислення кубів 100 чисел, що прискорює обробку на багатоядерних процесорах!