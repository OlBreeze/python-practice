import asyncio

async def micro_task():
    print("---Micro Task is starting...")
    await asyncio.sleep(1)
    print("---Micro Task is done...")

async def macro_task():
    print("-Macro Task is starting...")
    asyncio.create_task(micro_task())
    print("-Macro Task is continue...")
    await asyncio.sleep(1)
    print("-Macro Task is done...")

async def main():
    print("Starting main loop...")
    await macro_task()
    print("Main loop is done...")

# asyncio.run(main()) -# тестируем ниже код


# macro_task() запускает micro_task() через asyncio.create_task() —
# это микрозадача, которая выполняется параллельно, не блокируя макрозадачу.
#
# Обе задачи выполняются в рамках одного event loop.
# asyncio.run(main()) запускает цикл событий и завершает его, когда все задачи выполнены.
#
# 🔹 Вывод в консоль покажет пример асинхронного взаимодействия —
# микро-задача начнёт выполняться внутри макро-задачи, не дожидаясь её завершения.


loop = asyncio.get_event_loop()

loop.call_soon(lambda: print("Micro task is started..."))
loop.call_later(1, lambda: print("Macro task is started..."))

loop.run_until_complete(asyncio.sleep(2))
#
# loop.call_soon() — планирует выполнение микрозадачи
# (выполнится как можно скорее, на следующей итерации event loop).
#
# loop.call_later(1, ...) — планирует выполнение макрозадачи через 1 секунду.
#
# loop.run_until_complete(asyncio.sleep(2)) —
# запускает event loop на 2 секунды, чтобы дать задачам время выполниться.
