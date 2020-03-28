import asyncio
import uvloop
import random
import typing
from CoroutinesAndTasks.main import simple_coroutine

uvloop.install()

asyncio.locks.Lock()


def get_tasks(coro_func):
    tasks = []
    for i in range(10):
        tasks.append(coro_func(i))
    return tasks


async def simple_coroutine_with_lock(a, lock: asyncio.Lock):
    print("Wait lock")
    async with lock:
        print('Unlocked')
        await simple_coroutine(a)
        print("Task complete in lock")


async def simple_coroutine_with_event(a, event: asyncio.Event):
    print("Wait event")
    await event.wait()
    print("Event set")
    return await simple_coroutine(a)


async def simple_coroutine_with_condition(a, condition: asyncio.Condition):
    async with condition:
        print('Wait event')
        await condition.wait()
        print("Event set")
        await simple_coroutine(a)
        print("Task completed in condition", a)


async def simple_coroutine_with_dynamic_notify(condition: asyncio.Condition):
    notify = 0
    while notify < 10:
        await asyncio.sleep(random.uniform(0, 1))
        nd = random.randint(1, min(3, 10 - notify))
        async with condition:
            condition.notify(nd)
            print("Notified", nd)
        notify += nd


async def simple_coroutine_with_all_semaphores(a, semaphore: typing.Union[asyncio.Semaphore, asyncio.BoundedSemaphore]):
    print("Wait threads")
    async with semaphore:
        print("Unlocked")
        await simple_coroutine(a)
        print("Task completed in semaphore")


async def simple_coroutine_for_unlike_semaphores(semaphore: typing.Union[asyncio.Semaphore, asyncio.BoundedSemaphore]):
    for i in range(2):
        await semaphore.acquire()
    for i in range(10):
        try:
            semaphore.release()
        except ValueError:
            # For Bounded Semaphore acquire calls >= release calls not otherwise
            print("Its Bounded Semaphore")
            break
    else:
        print("Its Simple Semaphore")


async def main():
    # Lock
    lock = asyncio.Lock()
    tasks = get_tasks(lambda a: simple_coroutine_with_lock(a, lock))
    await asyncio.wait(tasks)

    # Event
    event = asyncio.Event()
    tasks = get_tasks(lambda a: simple_coroutine_with_event(a, event))
    await asyncio.sleep(1)
    event.set()
    await asyncio.wait(tasks)

    # Condition
    condition = asyncio.Condition()
    tasks = get_tasks(lambda a: simple_coroutine_with_condition(a, condition)) + [
        simple_coroutine_with_dynamic_notify(condition)]
    await asyncio.wait(tasks)

    # Simple Semaphore
    semaphore = asyncio.Semaphore(2)
    tasks = get_tasks(lambda a: simple_coroutine_with_all_semaphores(a, semaphore))
    await asyncio.wait(tasks)

    # Bounded Semaphore
    bounded_semaphore = asyncio.BoundedSemaphore(2)
    tasks = get_tasks(lambda a: simple_coroutine_with_all_semaphores(a, bounded_semaphore))
    await asyncio.wait(tasks)

    # For unlike the Simple and Bounded semaphore
    await simple_coroutine_for_unlike_semaphores(semaphore)
    await simple_coroutine_for_unlike_semaphores(bounded_semaphore)


if __name__ == '__main__':
    asyncio.run(main())
