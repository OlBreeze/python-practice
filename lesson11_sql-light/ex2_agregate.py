import sqlite3


# Класс для агрегации
class TotalRevenueAggregator:
    def __init__(self):
        self.total_revenue = 0

    def step(self, price, quantity):
        self.total_revenue += price * quantity

    def finalize(self):
        return self.total_revenue


# Подключение и регистрация агрегатной функции
conn = sqlite3.connect('shop.db')
conn.create_aggregate('total_revenue_per_product', 2, TotalRevenueAggregator)
cursor = conn.cursor()

# SQL запрос с агрегацией
cursor.execute('''SELECT o.product_id,
                         total_revenue_per_product(o.price, o.quantity)
                  FROM orders o
                           JOIN products p ON o.product_id = p.product_id
                  GROUP BY o.product_id''')

# Вывод результатов
results = cursor.fetchall()
for result in results:
    print(f"Product ID: {result[0]}, Total Revenue: {result[1]}")

conn.close()
#
# Что происходит:
# 
# create_aggregate() создает пользовательскую агрегатную функцию (как SUM или AVG)
# step() вызывается для каждой строки, накапливая выручку
# finalize() возвращает итоговый результат для каждой группы
# Запрос группирует заказы по продуктам и считает общую выручку