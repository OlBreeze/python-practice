def divide(a: int, b: int) -> float:
    """
    Ділить два числа.

    Args:
        a (int): Чисельник
        b (int): Знаменник

    Returns:
        float: Результат ділення

    Raises:
        ZeroDivisionError: Якщо знаменник дорівнює нулю
    """
    if b == 0:
        raise ZeroDivisionError("Ділення на нуль неможливе")
    return a / b