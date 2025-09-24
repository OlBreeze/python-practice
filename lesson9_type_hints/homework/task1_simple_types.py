# Завдання 1:
# Робота з простими типами
#
# Реалізуйте функцію calculate_discount, яка приймає:
# початкову ціну (price: float),
# відсоток знижки (discount: float),
# і повертає кінцеву ціну (float).
# Якщо знижка більше 100%, функція повинна повертати 0.

def calculate_discount(price: float, discount: float) -> float:
    """
    Обчислює кінцеву ціну товару після застосування знижки.

    :param price : float Початкова ціна товару.
    :param discount : float Відсоток знижки (від 0 до 100).

   :return: Кінцева ціна після застосування знижки.
    """
    if discount > 100:
        return 0.0

    final_price = price * (1 - discount / 100)
    return final_price

# Check in homework.py
# print(calculate_discount(100, 20))
# print(calculate_discount(100, 75))
# print(calculate_discount(100, 50))
# print(calculate_discount(50, 110))
