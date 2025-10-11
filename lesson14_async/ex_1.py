import time
import asyncio

async def task(name, delay):
    print(f"Start {name}!")
    await asyncio.sleep(delay)
    print(f"End {name}!")

async def main():
    await asyncio.gather(
        task("Task 1", 2),
        task("Task 2", 2)
    )

start = time.time()
asyncio.run(main())
print(f"Time: {time.time() - start:.2f} seconds")
