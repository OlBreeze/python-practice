# Завдання 7: Трекер витрат

total_expense = 0


def add_expense(amount: float):
    """Додає витрату до загальної суми"""
    global total_expense
    total_expense += amount


def get_expense() -> float:
    """Повертає загальну суму витрат"""
    return total_expense


while True:
    try:
        input_num = float(input("Введіть суму витрат або число 0 для виходу: "))
        if input_num == 0:
            print(f"Загальна сума витрат: {get_expense():.2f}")
            break
        add_expense(input_num)
    except ValueError:
        print("Помилка: введіть число!")
