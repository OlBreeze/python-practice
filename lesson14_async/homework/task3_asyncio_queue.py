# Асинхронні черги
# Реалізуйте асинхронну чергу завдань за допомогою asyncio.Queue.
# Створіть функцію producer(queue), яка додає 5 завдань
# до черги із затримкою в 1 секунду.
# Напишіть функцію consumer(queue), яка забирає завдання з черги,
# виконує його (наприклад, виводить повідомлення), імітуючи роботу
# з кожним завданням із затримкою в 2 секунди.
# Створіть функцію main(), яка одночасно запускає і producer,
# і кілька споживачів (consumer) за допомогою asyncio.gather(),
# щоб споживачі обробляли завдання в міру їх появи в черзі.

import asyncio
from typing import Any


async def producer(queue: asyncio.Queue, consumers_count: int) -> None:
    """
    Додає 5 завдань у чергу та надсилає сигнали завершення для споживачів.

    :param queue: Черга для завдань.
    :param consumers_count: Кількість споживачів (для завершальних сигналів).
    """
    for i in range(1, 6):
        task = f"Завдання {i}"
        await queue.put(task)
        print(f"[PRODUCER] Додано: {task}")
        await asyncio.sleep(1)

    # Сигнали завершення для кожного consumer
    for _ in range(consumers_count):
        # щоб споживачі розуміли, що це не завдання, а кінець
        await queue.put(None)


async def consumer(queue: asyncio.Queue, consumer_id: int) -> None:
    """
    Отримує та обробляє завдання з черги.

    :param queue: Асинхронна черга.
    :param consumer_id: Ідентифікатор споживача.
    """
    while True:
        task: Any = await queue.get()
        if task is None:
            print(f"[CONSUMER-{consumer_id}] Отримано сигнал завершення.")
            break

        print(f"[CONSUMER-{consumer_id}] Починає обробку: {task}")
        await asyncio.sleep(2)
        print(f"[CONSUMER-{consumer_id}] Завершив обробку: {task}")
        queue.task_done()


async def main() -> None:
    """
    Запускає producer і кілька consumer паралельно.
    """
    queue = asyncio.Queue()
    consumers_count = 3

    consumers = [consumer(queue, i + 1) for i in range(consumers_count)]

    await asyncio.gather(
        producer(queue, consumers_count),
        *consumers
    )


# ------------------------------------
if __name__ == "__main__":
    asyncio.run(main())

# queue.Queue(): Создает новую очередь.
# put(item): Помещает элемент item в очередь.
# get(): Извлекает и возвращает элемент из очереди.
# Если очередь пуста, метод блокируется до появления элементов.
# task_done(): Сообщает очереди, что задача,
# полученная с помощью get(), была полностью обработана.
# join(): Блокирует выполнение до тех пор, пока все
# элементы, помещенные в очередь,
# не будут обработаны. Это работает в паре с task_done().
