# Завдання 4: Таймер для тренування. Розробити програму, яка симулює таймер для тренувань
# із вбудованою функцією, що дозволяє змінювати час тренування на кожному кроці.
# Програма повинна виводити тривалість кожного раунду тренування.

default_time = 60


def training_session(rounds):
    """
    тривалість тренування
    :param rounds: кількість раундів тренування
    """
    time_per_round = default_time
    all_time_training = 0

    def adjust_time(num_round, dif=5):
        """дозволяє налаштовувати час для кожного окремого раунду"""
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
