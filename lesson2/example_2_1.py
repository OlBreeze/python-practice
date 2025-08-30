def outer_function():
    my_var = "enclosing"

    def inner_function():
        my_var = "inner"
        print(my_var)

    print(my_var)
    inner_function()
    print(my_var)

my_var = "global"
print(my_var)
outer_function()
print(my_var)