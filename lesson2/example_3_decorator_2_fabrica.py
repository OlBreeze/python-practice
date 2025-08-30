# Фабрика для декоратора, принимает параметр type_obj
def my_decorator_with_params(type_obj):
    # Сам декоратор, принимает декорируемую функцию func
    def my_decorator(func):
        # Обертка, которая выполняет дополнительную логику
        def wrapper(*args, **kwargs):
            print("Start working")

            # Вызываем оригинальную функцию и принудительно преобразуем результат
            # к типу, переданному в my_decorator_with_params
            result = type_obj(func(*args, **kwargs))

            print("End working")
            return result

        return wrapper

    return my_decorator


# Использование декоратора с параметром 'int'
@my_decorator_with_params(int)
def my_divide(a, b):
    return a / b


# Примеры вызовов
print(my_divide(1, 2))
print(my_divide(1, 3))
