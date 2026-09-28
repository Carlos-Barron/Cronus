import asyncio
import time

async def task(n: int) -> int:
    print(f" empieza {n}")
    #await asyncio.sleep(1)
    time.sleep(1)
    print(f" termina {n}")
    return n

async def sequential() -> list[int]:
    return [await task(1), await task(2), await task(3)]

async def concurrent() -> list[int]:
    return await asyncio.gather(task(1), task(2), task(3))

async def main() -> None:
    for name, func in (("Sequential", sequential), ("Concurrent", concurrent)):
        begin = time.perf_counter()
        result = await func()
        print(f"{name}: {result} in {time.perf_counter() - begin:.2f}s\n")


asyncio.run(main())