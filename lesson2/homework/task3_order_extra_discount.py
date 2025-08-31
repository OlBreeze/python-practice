# Завдання 3: Магазин замовлень з акційними знижками

discount = 0.1


def create_order(price: float):
    final_price = price * (1 - discount)
    print(f"Початкова ціна: {price}, після глобальної знижки {int(discount * 100)}%: {final_price}")

    def apply_additional_discount(extra_discount: float):
        nonlocal final_price
        final_price = final_price * (1 - extra_discount)
        print(f"Після додаткової знижки {int(extra_discount * 100)}%: {final_price}")
        return final_price

    return apply_additional_discount


order = create_order(1000)  # Початкова ціна: 1000, кінцева ціна зі знижкою 10%: 900
order(0.1)
order(0.05)
