class MyType1:
    x = 1.5
    c = 3

# Те саме визначення типу, але під час виконання за допомогою type()
MyType2 = type('MyType2', (object,), {'x': 1.5, 'c': 3})

print(MyType1)
print(type(MyType1))
print(MyType2)
print(type(MyType2))


# Два способа создания класса:
class A:
    x = 5

# Эквивалентно:
A2 = type('A2', (), {'x': 5})
