import threading
import random
import time
from typing import List


class Organism:
    """
    Клас, що представляє організм з основними характеристиками.
    """

    def __init__(self, energy: int = 10, age: int = 0):
        self.energy = energy
        self.age = age
        self.alive = True

    def live(self) -> List['Organism']:
        """
        Один цикл життя організму:
        споживання їжі, старіння, смерть, розмноження.

        :return: список нових нащадків (може бути порожнім)
        """
        if not self.alive:
            return []

        # Організм їсть (отримує енергію)
        food = random.randint(0, 5)
        self.energy += food

        # Старіння
        self.age += 1
        self.energy -= 2  # витрати енергії на життя

        if self.energy <= 0 or self.age > 10:
            self.alive = False
            print(f"💀 Організм помер (вік: {self.age}, "
                  f"енергія: {self.energy})")
            return []

        # Розмноження
        offspring = []
        if self.energy > 15 and random.random() < 0.3:
            self.energy -= 5
            child = Organism(energy=5)
            offspring.append(child)
            print(f"🍼 Новий організм народився! "
                  f"(від батька з енергією: {self.energy})")

        return offspring


def process_organism(org: Organism, new_offspring: List[Organism],
                     lock: threading.Lock) -> None:
    """
    Обробляє одного організму в окремому потоці.

    :param org: екземпляр організму
    :param new_offspring: загальний список нових нащадків
    :param lock: блокування для потокобезпечного доступу
    """
    offspring = org.live()
    with lock:
        new_offspring.extend(offspring)


def simulate_population(population: List[Organism],
                        generations: int = 10) -> None:
    """
    Запускає симуляцію популяції на задану кількість поколінь.

    :param population: початкова популяція
    :param generations: кількість поколінь (раундів)
    """
    lock = threading.Lock()

    for gen in range(1, generations + 1):
        print(f"\n🌱 Покоління {gen}, популяція: {len(population)}")
        threads = []
        new_organisms: List[Organism] = []

        for org in population:
            thread = threading.Thread(target=process_organism,
                                      args=(org, new_organisms, lock))
            thread.start()
            threads.append(thread)

        # Очікуємо завершення всіх потоків
        for t in threads:
            t.join()

        # Видаляємо мертвих
        population = [org for org in population if org.alive]

        # Додаємо нових
        population.extend(new_organisms)

        # Затримка для реалістичності
        time.sleep(0.5)

    print(f"\nСимуляцію завершено. Кінцева популяція: {len(population)}")


# ----let's go! )))-----------------
if __name__ == "__main__":
    initial_population = [Organism() for _ in range(10)]
    simulate_population(initial_population, generations=10)
