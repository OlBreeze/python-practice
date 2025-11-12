from django.db import models

# Кастомное поле: автоматически сохраняет текст в ВЕРХНЕМ регистре
class UpperCaseCharField(models.CharField):
    def get_prep_value(self, value):
        if value:
            return value.upper()
        return value

class Product(models.Model):
    name = UpperCaseCharField(max_length=100) # !!!
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    def total_value(self):
        """Возвращает общую стоимость (цена × количество)"""
        return self.price * self.quantity

    def __str__(self):
        return f"{self.name} ({self.quantity} шт.)"
