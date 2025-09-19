#     !!!!
# doctest — это когда прямо в докстринге функции пишутся примеры её работы, и
# Python сам может проверить, что результат совпадает.

import doctest

def divide(a: int, b: int) -> int:
    """
    Ділить a на b з цілочисельним результатом.

    Приклади:
    >>> divide(20, 4)
    5
    >>> divide(4, 2)
    2
    >>> divide(5, 2)
    2

    Якщо поділити на 0:
    >>> divide(10, 0)
    Traceback (most recent call last):
    ...
    ValueError: Ділення на 0!!!
    """
    if b == 0:
        raise ValueError("Ділення на 0!!!")
    return a // b


if __name__ == "__main__":
    doctest.testmod()


