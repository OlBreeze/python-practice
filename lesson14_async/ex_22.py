import asyncio

async def main():
    loop = asyncio.get_running_loop()

    loop.call_soon(lambda: print("Micro task is started..."))
    loop.call_later(1, lambda: print("Macro task is started..."))

    await asyncio.sleep(2)

asyncio.run(main())

# 🔍 Что изменилось:
# asyncio.run(main()) — сам создаёт и закрывает event loop.
#
# get_running_loop() — получает текущий активный цикл событий, вместо устаревшего get_event_loop().
#
# ⚡ Теперь код работает без DeprecationWarning и полностью совместим с новыми версиями Python.