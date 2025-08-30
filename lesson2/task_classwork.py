import time


def my_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        timer = end - start
        print(f"Час: {timer}")

    return wrapper


@my_decorator
def sum_range(r_start, r_end):
    print(f"Сума: {sum(range(r_start, r_end))}")


sum_range(1, 10000)
sum_range(1, 100000)
