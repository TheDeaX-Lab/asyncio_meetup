import asyncio
import uvloop
from CoroutinesAndTasks.main import simple_coroutine

uvloop.install()


async def simple_coroutine_with_shield():
    await asyncio.shield(simple_coroutine(1))


async def main():
    # Timeout
    coro = simple_coroutine_with_shield()
    try:
        await asyncio.wait_for(coro, 0.2)
    except asyncio.TimeoutError:
        print("Timeout Error!!!")
    await asyncio.sleep(1)

    # Cancelled
    task = asyncio.create_task(simple_coroutine_with_shield())
    try:
        await asyncio.sleep(0.1)
        task.cancel()
        await task
    except asyncio.CancelledError:
        print("Cancelled Error!!!")
    await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
