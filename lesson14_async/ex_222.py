import asyncio

async def micro():
    print("  → Микрозадача start")
    await asyncio.sleep(0)
    print("  → Микрозадача end")

async def macro():
    print("Макрозадача start")
    await micro()
    print("Макрозадача end")

asyncio.run(macro())