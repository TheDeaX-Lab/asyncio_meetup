import asyncio
import uvloop
from CoroutinesAndTasks.main import simple_coroutine_with_exception, simple_coroutine

uvloop.install()


def callback(task: asyncio.Task):
    if task.cancelled():
        print("Task is cancelled")
    else:
        try:
            print("Task is done", task.result())
        except:
            print("Task raised", task.exception())


async def main():
    task = asyncio.create_task(simple_coroutine(1))
    # Can cancel execute
    # task.cancel()

    # Is completed?
    # task.done()

    # Is cancelled?
    # task.cancelled()

    # Get result (Notice can raise exception)
    # task.result()

    # Get exception (If you know that is exception, otherwise None)
    # task.exception()

    # Can add callback
    task.add_done_callback(callback)
    await asyncio.sleep(1)
    # Can remove callback
    task.remove_done_callback(callback)


if __name__ == '__main__':
    asyncio.run(main())
