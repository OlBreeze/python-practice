from abc import ABC, abstractmethod


# === ЧТО ТАКОЕ АБСТРАКТНЫЕ КЛАССЫ ===

# 1. АБСТРАКТНЫЙ КЛАСС - нельзя создать экземпляр
class Animal(ABC):  # Наследуется от ABC

    @abstractmethod  # Абстрактный метод - ОБЯЗАН быть реализован в дочерних классах
    def make_sound(self):
        pass  # Нет реализации

    @abstractmethod
    def move(self):
        pass

    # Обычный метод - может иметь реализацию
    def sleep(self):
        print("Животное спит...")


# 2. КОНКРЕТНЫЕ КЛАССЫ - наследники абстрактного класса
class Dog(Animal):
    # ОБЯЗАТЕЛЬНО реализуем все абстрактные методы
    def make_sound(self):
        return "Гав!"

    def move(self):
        return "Бежит на четырех лапах"


class Bird(Animal):
    def make_sound(self):
        return "Чирик!"

    def move(self):
        return "Летит"


# 3. ДЕМОНСТРАЦИЯ РАБОТЫ
print("=== Создание экземпляров ===")

# Попытка создать абстрактный класс - ОШИБКА!
try:
    animal = Animal()
except TypeError as e:
    print(f"Ошибка: {e}")

# Создаем конкретные объекты - OK!
dog = Dog()
bird = Bird()

print(f"Собака: {dog.make_sound()}, {dog.move()}")
print(f"Птица: {bird.make_sound()}, {bird.move()}")

# Наследованный метод работает
dog.sleep()
bird.sleep()

print("\n" + "=" * 50)


# === ПРИМЕР ИЗ ПРАКТИКИ: ФИГУРЫ ===
class Shape(ABC):
    @abstractmethod
    def area(self):
        """Вычисляет площадь фигуры"""
        pass

    @abstractmethod
    def perimeter(self):
        """Вычисляет периметр фигуры"""
        pass

    # Конкретный метод
    def description(self):
        return f"Это фигура с площадью {self.area():.2f} и периметром {self.perimeter():.2f}"


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius


# Использование
print("=== Фигуры ===")
rectangle = Rectangle(5, 3)
circle = Circle(4)

print(rectangle.description())
print(circle.description())

# === НЕПОЛНАЯ РЕАЛИЗАЦИЯ - ОШИБКА ===
print("\n=== Неполная реализация ===")


class IncompleteShape(Shape):
    def area(self):
        return 10
    # НЕ реализовали perimeter() - будет ошибка!


try:
    incomplete = IncompleteShape()
except TypeError as e:
    print(f"Ошибка: {e}")

print("\n" + "=" * 50)


# === ПОЛИМОРФИЗМ С АБСТРАКТНЫМИ КЛАССАМИ ===
def print_shape_info(shape: Shape):  # Принимает любой Shape
    print(f"Площадь: {shape.area():.2f}")
    print(f"Периметр: {shape.perimeter():.2f}")
    print(f"Описание: {shape.description()}")
    print("-" * 30)


print("=== Полиморфизм ===")
shapes = [Rectangle(4, 6), Circle(3), Rectangle(2, 8)]

for shape in shapes:
    print_shape_info(shape)

print("\n" + "=" * 50)


# === АЛЬТЕРНАТИВА БЕЗ ABC (не рекомендуется) ===
class OldStyleAnimal:  # Без ABC
    def make_sound(self):
        raise NotImplementedError("Подкласс должен реализовать make_sound()")


class OldDog(OldStyleAnimal):
    def make_sound(self):
        return "Гав!"


print("=== Старый стиль (без ABC) ===")
# Можно создать экземпляр, но вызов метода даст ошибку
old_animal = OldStyleAnimal()  # Создается без ошибки!
try:
    old_animal.make_sound()  # Ошибка только при вызове
except NotImplementedError as e:
    print(f"Ошибка при вызове: {e}")

old_dog = OldDog()
print(f"Старая собака: {old_dog.make_sound()}")

print("\n" + "=" * 50)

# === ПРЕИМУЩЕСТВА ABC ===
print("=== ПРЕИМУЩЕСТВА ИСПОЛЬЗОВАНИЯ ABC ===")
print("✓ Ошибка обнаруживается при создании объекта, а не при вызове метода")
print("✓ Четко определяет контракт для наследников")
print("✓ Улучшает читаемость кода")
print("✓ Помогает IDE с автодополнением")
print("✓ Облегчает рефакторинг")
print("✓ Документирует намерения программиста")

# === ISINSTANCE РАБОТАЕТ С ABC ===
print(f"\ndog является Animal: {isinstance(dog, Animal)}")
print(f"rectangle является Shape: {isinstance(rectangle, Shape)}")
print(f"dog является Shape: {isinstance(dog, Shape)}")