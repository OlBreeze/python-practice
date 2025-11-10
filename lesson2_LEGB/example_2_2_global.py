def outer_function():
    my_var = "enclosing"

    def inner_function():
        global my_var
        print(f"inside outer function:{my_var}")
        my_var = "local"
        print(my_var)

    print(my_var)
    inner_function()
    print(my_var)

my_var = "global"
print(my_var)
outer_function()
print(my_var)