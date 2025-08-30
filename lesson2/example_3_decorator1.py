def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Start working")
        func(*args, **kwargs)
        print("End working")

    return wrapper


@my_decorator
def my_function():
    print("Hello World")


@my_decorator
def my_divide(a, b):
    print(f"Hello. Result: {a / b}")


my_divide(1, 2)
my_divide(1, 3)
