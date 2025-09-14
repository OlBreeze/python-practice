def my_generator(n):  # usage
    for digit in range(n):
        yield digit #возвращает значение и "приостанавливает" выполнение функции

for element in my_generator(5):
    print(element)

print(list(my_generator(15)))