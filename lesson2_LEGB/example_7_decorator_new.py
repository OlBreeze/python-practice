# ПАТТЕРН ДЕКОРАТОР - пример с кофе

from abc import ABC, abstractmethod


# Базовый интерфейс для всех напитков
class Coffee(ABC):
    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_cost(self):
        pass


# Базовый класс кофе
class Cappuccino(Coffee):
    def get_description(self):
        return "Cappuccino"

    def get_cost(self):
        return 3.0


class Espresso(Coffee):
    def get_description(self):
        return "Espresso"

    def get_cost(self):
        return 2.0


class Americano(Coffee):
    def get_description(self):
        return "Americano"

    def get_cost(self):
        return 2.5


# Базовый декоратор
class CoffeeDecorator(Coffee):
    def __init__(self, coffee):
        self._coffee = coffee

    def get_description(self):
        return self._coffee.get_description()

    def get_cost(self):
        return self._coffee.get_cost()


# Конкретные декораторы (добавки)
class SugarDecorator(CoffeeDecorator):
    def get_description(self):
        return self._coffee.get_description() + " + Sugar"

    def get_cost(self):
        return self._coffee.get_cost() + 0.2


class MilkDecorator(CoffeeDecorator):
    def get_description(self):
        return self._coffee.get_description() + " + Milk"

    def get_cost(self):
        return self._coffee.get_cost() + 0.5


class CinnamonDecorator(CoffeeDecorator):
    def get_description(self):
        return self._coffee.get_description() + " + Cinnamon"

    def get_cost(self):
        return self._coffee.get_cost() + 0.3


class VanillaDecorator(CoffeeDecorator):
    def get_description(self):
        return self._coffee.get_description() + " + Vanilla"

    def get_cost(self):
        return self._coffee.get_cost() + 0.4


class WhippedCreamDecorator(CoffeeDecorator):
    def get_description(self):
        return self._coffee.get_description() + " + Whipped Cream"

    def get_cost(self):
        return self._coffee.get_cost() + 0.7


# Демонстрация использования
print("=== КОФЕЙНАЯ ЛАВКА ===\n")

# Простой капучино
cappuccino_basic = Cappuccino()
print(f"1. {cappuccino_basic.get_description()}")
print(f"   Цена: ${cappuccino_basic.get_cost():.2f}")
print()

# Капучино с сахаром (как на скриншоте)
cappuccino_with_sugar = SugarDecorator(Cappuccino())
print(f"2. {cappuccino_with_sugar.get_description()}")
print(f"   Цена: ${cappuccino_with_sugar.get_cost():.2f}")
print()

# Изысканный эспрессо с корицей и молоком (как на скриншоте)
fancy_espresso = CinnamonDecorator(SugarDecorator(MilkDecorator(Espresso())))
print(f"3. {fancy_espresso.get_description()}")
print(f"   Цена: ${fancy_espresso.get_cost():.2f}")
print()

# Сложный заказ - Американо с множеством добавок
complex_order = WhippedCreamDecorator(
    VanillaDecorator(
        CinnamonDecorator(
            SugarDecorator(
                MilkDecorator(Americano())
            )
        )
    )
)
print(f"4. {complex_order.get_description()}")
print(f"   Цена: ${complex_order.get_cost():.2f}")
print()

print("=== Различные комбинации ===")

# Эспрессо с сахаром и взбитыми сливками
espresso_sweet = WhippedCreamDecorator(SugarDecorator(Espresso()))
print(f"• {espresso_sweet.get_description()}")
print(f"  Цена: ${espresso_sweet.get_cost():.2f}")

# Капучино с ванилью и корицей
cappuccino_spiced = CinnamonDecorator(VanillaDecorator(Cappuccino()))
print(f"• {cappuccino_spiced.get_description()}")
print(f"  Цена: ${cappuccino_spiced.get_cost():.2f}")

print("\n=== Преимущества паттерна Декоратор ===")
print("✓ Можно добавлять функциональность динамически")
print("✓ Можно комбинировать декораторы в любом порядке")
print("✓ Легко добавлять новые декораторы")
print("✓ Не нужно создавать классы для всех возможных комбинаций")
print("✓ Соответствует принципу открытости/закрытости")

# Демонстрация гибкости
print(f"\n=== Создание заказа пошагово ===")
order = Cappuccino()
print(f"Базовый заказ: {order.get_description()} - ${order.get_cost():.2f}")

order = SugarDecorator(order)
print(f"+ Сахар: {order.get_description()} - ${order.get_cost():.2f}")

order = MilkDecorator(order)
print(f"+ Молоко: {order.get_description()} - ${order.get_cost():.2f}")

order = CinnamonDecorator(order)
print(f"+ Корица: {order.get_description()} - ${order.get_cost():.2f}")

print(f"\nИтоговый заказ: {order.get_description()}")
print(f"Итоговая цена: ${order.get_cost():.2f}")