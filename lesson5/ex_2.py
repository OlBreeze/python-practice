class MetaPerson(type):
    def __repr__(cls):
        return "Person"

    def __new__(meta_person, future_class_name, future_class_parents, future_class_attr):
        uppercase_attr = {}
        for name, val in future_class_attr.items():
            if not name.startswith('__'):
                uppercase_attr[name.upper()] = val
            else:
                uppercase_attr[name] = val

        # повторно використовуємо метод type.__new__, це базове ООП, в ньому немає нічого чарівного
        return type.__new__(meta_person, future_class_name, future_class_parents, uppercase_attr)


# Процес створення класу можна налаштувати, передавши ключовий аргумент metaclass в рядку визначення класу або
# наслідувавши від існуючого класу, який включає такий аргумент. Клас Person та UpdatePerson є екземплярами MetaPerson
# будь-які інші ключові аргументи, зазначені в визначенні класу, передаються у всі операції metaclass, описані нижче.

# Metaclass в Python — это "класс для создания классов".
# Если класс определяет, как создавать объекты, то метакласс определяет, как создавать классы.

class Person(metaclass=MetaPerson):
    def __init__(self, surname, name, age, friends):
        self.surname = surname
        self.name = name
        self.age = age
        self.friends = friends

    def get_friends(self):
        return self.friends

class UpdatePerson(Person):
    pass

p = Person(surname="Dmytrenko", name="Dmytro", age=18, friends=["Ivanenko", "Petrenko"])
print(type(p))
print(f"im'я Person є екземпляром метакласу {type(Person)}")
print(type(Person))
print("<class 'function'>")
print(type(getattr(Person, "GET_FRIENDS")))
print(True)
print(isinstance(p, Person))
print(False)
print(isinstance(p, MetaPerson))
print("Person")
print(p.__class__)
print(p.__dict__)
print(p.__class__.__dict__)
print({k: v.__class__ for k, v in p.__dict__.items()})