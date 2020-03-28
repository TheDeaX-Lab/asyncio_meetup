from CoroutinesAndTasks.main import simple_coroutine, simple_coroutine_with_exception
import asyncio
import uvloop

uvloop.install()


def get_tasks():
    tasks = []
    for i in range(5):
        tasks.append(simple_coroutine(i))
    return tasks


# Results iteriable coros order by first completed
async def concurrent_with_ascompleted():
    tasks = get_tasks()
    for coro in asyncio.as_completed(tasks):
        value = await coro
        print(value)
    print("Completed Concurrent with as_completed")


# Results order by first completed, waiting with params
async def concurrent_with_wait():
    # Variant All completed
    tasks = get_tasks()
    done, _ = await asyncio.wait(tasks)
    for coro in done:
        value = await coro
        print(value)
    print("Variant All completed")

    # Variant First completed
    tasks = get_tasks()
    (coro, *_), pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    value = await coro
    print(value)
    print("Variant First completed")

    # Variant First exception
    tasks = get_tasks()
    tasks.insert(2, simple_coroutine_with_exception(1))
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
    for coro in done:
        try:
            value = await coro
        except Exception as e:
            print("Error catched", e)
    print("Variant First exception")


# Results order by list indexes, waiting all
async def concurrent_with_gather():
    tasks = get_tasks()
    values = await asyncio.gather(*tasks)
    for value in values:
        print(value)
    print("Concurrent with gather completed")


async def main():
    await concurrent_with_ascompleted()
    await concurrent_with_wait()
    await concurrent_with_gather()


if __name__ == '__main__':
    asyncio.run(main())
