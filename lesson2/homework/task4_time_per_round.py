# Завдання 4: Таймер для тренування. Розробити програму, яка симулює таймер для тренувань
# із вбудованою функцією, що дозволяє змінювати час тренування на кожному кроці.
# Програма повинна виводити тривалість кожного раунду тренування.

default_time: int = 60


def training_session(rounds: int) -> int:
    """
    Створює сесію тренування із можливістю регулювання тривалості
    кожного раунду за допомогою вкладеної функції.
    Parameters
    ----------
    rounds : int
        Кількість раундів у тренуванні.
    Returns
    -------
    int
        Загальний час у хвилинах, витрачений на всі раунди тренування.
    """
    time_per_round: int = default_time
    all_time_training: int = 0

    def adjust_time(num_round: int, dif: int = 5):
        """
        дозволяє налаштовувати час для кожного окремого раунду
        Parameters
        ----------
        num_round : int
            Номер поточного раунду (починається з 0).
        dif : int, optional
            Величина зменшення часу в хвилинах (за замовчуванням 5).
        """
        nonlocal time_per_round
        nonlocal all_time_training
        if num_round != 0:
            time_per_round -= dif
        print(f"Раунд {num_round + 1}: {time_per_round} хвилин")
        all_time_training += time_per_round

    for i in range(rounds):
        adjust_time(i)

    return all_time_training


all_time = training_session(5)
print(f"------------------------\nВесь час тренування: {all_time}")

#
# Раунд 1: 60 хвилин
# Раунд 2: 55 хвилин
# Раунд 3: 50 хвилин
# Раунд 4: 45 хвилин
# Раунд 5: 40 хвилин
# ------------------------
# Весь час тренування: 250
