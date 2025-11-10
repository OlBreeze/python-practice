import sys

class Example():
    def __new__(cls, *args, **kwargs):
        new_product = object.__new__(cls)
        print("Example __new__ gets called")
        return new_product

    def __init__(self, *args, **kwargs):
        print("Example __init__ gets called")

    def __del__(self):
        print("Example __del__ gets called")

    def __str__(self):
        return "Example __str__ gets called"

    def __call__(self, *args, **kwargs):
        print("Example __call__ gets called")

ex1 = Example()
print("refcount:", sys.getrefcount(ex1))
print("refcount:", sys.getrefcount(ex1))

print("refcount:", sys.getrefcount(ex1)) # The sys.getrefcount() function itself temporarily creates one more reference to the object,
# to check it. This reference exists only at the moment the function is called.
# Therefore, the counter will always be 1 higher than you expect.
ex2 = Example()
ex23 = ex2
print("refcount:", sys.getrefcount(ex2))

print(ex1())
#
# Этот пример кода демонстрирует, как работают специальные методы классов в Python,
# а также концепцию **счётчика ссылок** для управления памятью.
#
# ### 1. Специальные методы класса (`dunder methods`)
#
# Пример показывает, как переопределить несколько "магических" методов (начинаются и заканчиваются двойным подчёркиванием), которые позволяют настроить поведение объекта:
# * `__new__(cls, ...)`: Это первый метод, который вызывается при создании нового экземпляра класса.
#       Он отвечает за выделение памяти для объекта и возвращает новый экземпляр.
# * `__init__(self, ...)`: Инициализирует созданный объект. Он получает экземпляр, возвращённый `__new__`,
#   и настраивает его начальное состояние.
# * `__str__(self)`: Определяет строковое представление объекта, которое вызывается
#   функцией `print()` или `str()`.
# * `__del__(self)`: Финализатор. Вызывается, когда объект собирается быть уничтоженным сборщиком мусора.
#   Это происходит, когда счётчик ссылок на объект достигает нуля.
#
# ### 2. Управление памятью и счётчик ссылок
#
# Код демонстрирует, как работает счётчик ссылок в Python:
# * `sys.getrefcount(obj)`: Эта функция показывает, сколько раз на объект `obj` ссылается переменная или другой объект. Когда счётчик достигает нуля, объект может быть удалён из памяти.
# * **Важный нюанс**: Как указано в комментариях кода, сама функция `sys.getrefcount()` временно создаёт ещё одну ссылку на объект, чтобы получить его значение. Поэтому возвращаемое значение всегда будет на 1 больше, чем вы могли бы ожидать.
# * `ex2 = Example()`: Создаётся новый объект. Счётчик ссылок на него равен 1 (плюс 1 временная от `getrefcount`).
# * `ex23 = ex2`: Присваивание переменной `ex2` переменной `ex23` создаёт ещё одну ссылку на тот же объект, поэтому счётчик ссылок увеличивается.