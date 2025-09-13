my_list = [1, 2, 3, 4, 5]
my_iter_object = iter(my_list)
print(my_iter_object)
print(next(my_iter_object))

print()

my_iter_object = iter(my_list)

while True:
    try:
        print(next(my_iter_object))
    except StopIteration:
        break