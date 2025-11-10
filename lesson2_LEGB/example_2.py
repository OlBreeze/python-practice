def outer_function():
    my_var = 1000

    def inner_function():
        print(my_var)

    print(my_var)
    inner_function()
    print(my_var)

my_var = 100
print(my_var)
outer_function()
print(my_var)