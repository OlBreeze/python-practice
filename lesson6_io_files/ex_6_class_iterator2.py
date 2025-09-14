class IntegerGenerator:  # 2 usages
    """
    Клас-ітератор, що генерує послідовність цілих чисел.
    """

    def __init__(self, start, stop, step=1):
        """
        Ініціалізує ітератор.

        :param start: Початкове значення.
        :param stop: Кінцеве значення (не включається).
        :param step: Крок.
        """
        self.current = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        """
        Повертає сам об'єкт-ітератор.
        """
        return self

    def __next__(self):
        """
        Повертає наступне ціле число в послідовності.
        """
        if self.step > 0 and self.current < self.stop:
            result = self.current
            self.current += self.step
            return result
        elif self.step < 0 and self.current > self.stop:
            result = self.current
            self.current += self.step
            return result
        else:
            raise StopIteration

# Приклад використання в циклі for
print("Генерація чисел від 1 до 10 з кроком 2:")
for number in IntegerGenerator(start=1, stop=10, step=2):
    print(number)  # Виведе: 1, 3, 5, 7, 9

print("-" * 100)

# Приклад перетворення в список
generator_list = list(IntegerGenerator(start=10, stop=1, step=-1))
print("Перетворення в список чисел від 10 до 1 з кроком -1:")
print(generator_list)  # Виведе: [10, 9, 8, 7, 6, 5, 4, 3, 2]

    # Приклад перетворення в список