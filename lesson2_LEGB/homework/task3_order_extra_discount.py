# Завдання 3: Магазин замовлень з акційними знижками

discount: float = 0.1


def create_order(price: float):
    """
    Створює замовлення з урахуванням глобальної знижки та повертає функцію
    для застосування додаткових індивідуальних знижок.

    Parameters
    ----------
    price : float
        Початкова ціна товару.

    Returns
    -------
    Callable[[float], float]
        Функція, яка приймає додаткову знижку (у вигляді дробу, наприклад 0.1 = 10%)
        та повертає кінцеву ціну після її застосування.
    """
    final_price: float = price * (1 - discount)
    print(f"Початкова ціна: {price}, після глобальної знижки {int(discount * 100)}%: {final_price}")

    def apply_additional_discount(extra_discount: float) -> float:
        """
        Застосовує додаткову знижку до замовлення.

        Parameters
        ----------
        extra_discount : float
            Розмір знижки у вигляді десяткового дробу (наприклад, 0.2 = 20%).

        Returns
        -------
        float
            Кінцева ціна після застосування додаткової знижки.
        """
        nonlocal final_price
        final_price = final_price * (1 - extra_discount)
        print(f"Після додаткової знижки {int(extra_discount * 100)}%: {final_price}")
        return final_price

    return apply_additional_discount


order = create_order(1000)  # Початкова ціна: 1000, кінцева ціна зі знижкою 10%: 900
order(0.1)
order(0.05)
