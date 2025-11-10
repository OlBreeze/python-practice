# Фабрика для декоратора, принимает параметр type_obj (в данном случае 'repr')
def my_decorator_with_params(type_obj):
    # Декоратор, принимает декорируемую функцию func
    def my_decorator(func):
        # Обертка, которая выполняет дополнительную логику
        def wrapper(*args, **kwargs):
            # Вызываем оригинальную функцию и передаем ее результат в repr()
            result = type_obj(func(*args, **kwargs))
            return result

        return wrapper

    return my_decorator


# Использование декоратора с функцией repr
@my_decorator_with_params(repr)
def my_divide(a, b):
    return a / b


# Вызовы
print(type(my_divide(1, 2)))
print(type(my_divide(1, 3)))