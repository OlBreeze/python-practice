class Beverage:
    def get_cost(self)->float:
        pass

    def get_description(self):
        pass


class Espresso(Beverage):
    def get_cost(self):
        return 2.5

    def get_description(self):
        return 'Espresso'


class Cappuccino(Beverage):
    def get_cost(self):
        return 3.5

    def get_description(self):
        return 'Cappuccino'


class IngredientDecorator(Beverage):
    def __init__(self, beverage: Beverage):
        self.beverage = beverage

    def get_cost(self):
        return self.beverage.get_cost()

    def get_description(self):
        return self.beverage.get_description()


class MilkDecorator(IngredientDecorator):
    def get_cost(self):
        return self.beverage.get_cost() + 0.5

    def get_description(self):
        return f"{self.beverage.get_description()}, Milk"


class SugarDecorator(IngredientDecorator):
    def get_cost(self):
        return self.beverage.get_cost() + 0.25

    def get_description(self):
        return f"{self.beverage.get_description()}, Sugar"


class CinnamonDecorator(IngredientDecorator):
    def get_cost(self):
        return self.beverage.get_cost() + 0.75

    def get_description(self):
        return f"{self.beverage.get_description()}, Cinnamon"


espresso = Espresso()
print(f"Desc: {espresso.get_description()}")
print(f"Cost: {espresso.get_cost()}")


cappuccino_with_sugar = SugarDecorator(Cappuccino())
print(f"Description: {cappuccino_with_sugar.get_description()}")
print(f"Cost: {cappuccino_with_sugar.get_cost()}")

fancy_espresso = CinnamonDecorator(SugarDecorator(MilkDecorator(Espresso())))
print(f"Description: {fancy_espresso.get_description()}")
print(f"Cost: {fancy_espresso.get_cost()}")
