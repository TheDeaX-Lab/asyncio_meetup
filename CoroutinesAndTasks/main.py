import asyncio
import uvloop
import random

uvloop.install()


async def simple_coroutine(a):
    await asyncio.sleep(random.uniform(0, 1))  # Здесь могла бы быть любая функция которая требует ожидания результата
    print(f"Completed {a}")
    return a


async def simple_coroutine_with_exception(a):
    await asyncio.sleep(random.uniform(0, 1))
    raise Exception(a)


async def main():
    # Simple get result of coroutine
    value = await simple_coroutine(1)

    # Catching exception of coroutine
    try:
        value = await simple_coroutine_with_exception(1)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    asyncio.run(main())
