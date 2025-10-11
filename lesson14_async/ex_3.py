import asyncio

async def waiter(event: asyncio.Event, future: asyncio.Future):
    print("listen task: I'm waiting for event...")
    await event.wait()
    print("listen task: I'm done! Start transform...")
    await asyncio.sleep(1)
    result = "transform is done!"
    future.set_result(result)
    print("listen task: I'm done! End transform...")

async def controller(event: asyncio.Event, future: asyncio.Future):
    print("controller task: I'm waiting for event...")
    await asyncio.sleep(2)
    print("controller task: I'm done! Let's continue")
    event.set()


async def observer(event: asyncio.Event, future: asyncio.Future):
    print("observer task: I'm waiting for event...")

    # Зупиняє виконання, доки Future не отримає результат
    result = await future

    print(f"observer task: I'm done! {result}")


async def main():
    event = asyncio.Event()
    future = asyncio.Future()

    # waiter_task = asyncio.create_task(waiter(event, future))
    # controller_task = asyncio.create_task(controller(event, future))
    # observer_task = asyncio.create_task(observer(event, future))
    #
    # await asyncio.gather(waiter_task, controller_task, observer_task)

    await asyncio.gather(waiter(event, future),
                         controller(event, future),
                         observer(event, future))

    print("Final result:", future.result())

asyncio.run(main())
#
# asyncio.Event() — объект-сигнал, который можно "ждать" с помощью await event.wait().
#
# Пока event.set() не вызван, ожидающие задачи приостановлены.
#
# После event.set() все, кто ждал этот event, продолжают выполнение.
#
# asyncio.Future() используется, чтобы сохранить результат асинхронной операции и получить его позже.