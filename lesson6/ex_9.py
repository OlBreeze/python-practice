my_list = [1, 2, 3, 4, 5]

print([digit ** 2 for digit in my_list])  # список, создаёт список сразу в памяти.

my_gen = (digit ** 2 for digit in my_list)  # генератор, создаёт генератор, который выдаёт элементы по одному (экономит память)

for digit in my_gen:
    print(digit)
