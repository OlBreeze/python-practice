# #Завдання 11: Метаклас для обмеження кількості атрибутів (опціонально)
# Реалізуйте метаклас LimitedAttributesMeta, який дозволяє класам мати лише фіксовану кількість атрибутів (наприклад, максимум 3). Якщо додати більше атрибутів, має виникати помилка.
# Приклад виконання:
# Copy code
# class LimitedClass(metaclass=LimitedAttributesMeta):
#     attr1 = 1
#     attr2 = 2
#     attr3 = 3
#     # attr4 = 4  # Викличе помилку
#
#
# obj = LimitedClass()
# Очікуваний результат:
# TypeError: Клас LimitedClass не може мати більше 3 атрибутів.
# Завдання 12: Автоматичне логування доступу до атрибутів (опціонально)
# Створіть метаклас LoggingMeta, який автоматично додає логування при доступі до будь-якого атрибута класу. Кожен раз, коли атрибут змінюється або читається, повинно з'являтися повідомлення в консолі.
# Приклад виконання:
# Copy code
# class MyClass(metaclass=LoggingMeta):
#     def __init__(self, name):
#         self.name = name
#
#
# obj = MyClass("Python")
# print(obj.name)  # Logging: accessed 'name'
# obj.name = "New Python"  # Logging: modified 'name'
# Очікуваний результат:
# Logging: accessed 'name'
# Logging: modified 'name'
# Завдання 13: Автоматична генерація методів для полів класу (опціонально)
# Реалізуйте метаклас AutoMethodMeta, який автоматично генерує методи геттера та сеттера для кожного атрибута класу. Метод повинен починатися з get_<attribute>() та set_<attribute>(value).
# Приклад виконання:
# Copy code
# class Person(metaclass=AutoMethodMeta):
#     name = "John"
#     age = 30
#
#
# p = Person()
# print(p.get_name())  # John
# p.set_age(31)
# print(p.get_age())  # 31
# Очікуваний результат:
# John
# 31
# Завдання 14: Метаклас для перевірки типів полів (опціонально)
# Задача: Реалізуйте метаклас TypeCheckedMeta, який перевіряє типи атрибутів при їх встановленні. Якщо тип значення не відповідає типовому опису, має виникати помилка.
# Приклад виконання:
# Copy code
# class Person(metaclass=TypeCheckedMeta):
#     name: str = ""
#     age: int = 0
#
#
# p = Person()
# p.name = "John"  # Все добре
# p.age = "30"     # Викличе помилку, очікується int
# Очікуваний результат:
# TypeError: Для атрибута 'age' очікується тип 'int', але отримано 'str'.
#
