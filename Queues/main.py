import asyncio
import uvloop
import typing
import random

uvloop.install()


async def simple_coroutine_consumer_queue(queue: typing.Union[asyncio.Queue, asyncio.LifoQueue], event: asyncio.Event):
    while True:
        if queue.qsize() == 0 and event.is_set():
            break
        item = await queue.get()
        print(item)
    event.clear()


async def simple_coroutine_feeder_queue(queue: typing.Union[asyncio.Queue, asyncio.LifoQueue], event: asyncio.Event):
    for i in range(25):
        await queue.put(i)
    event.set()


async def simple_coroutine_consumer_queue_with_priority(queue: asyncio.PriorityQueue,
                                                        event: asyncio.Event):
    while True:
        if queue.qsize() == 0 and event.is_set():
            break
        item = await queue.get()
        print(f"Priority {item[0]} value {item[1]}")
    event.clear()


async def simple_coroutine_feeder_queue_with_priority(queue: asyncio.PriorityQueue,
                                                      event: asyncio.Event):
    for i in range(25):
        await queue.put((random.randint(0, 1000), i))
    event.set()


async def main():
    event = asyncio.Event()

    print("With simple queue")
    queue = asyncio.Queue(10)
    tasks = [simple_coroutine_consumer_queue(queue, event), simple_coroutine_feeder_queue(queue, event)]
    await asyncio.wait(tasks)

    print("With lifo queue")
    lifo_queue = asyncio.LifoQueue(10)
    tasks = [simple_coroutine_consumer_queue(lifo_queue, event), simple_coroutine_feeder_queue(lifo_queue, event)]
    await asyncio.wait(tasks)

    priority_queue = asyncio.PriorityQueue(10)
    tasks = [simple_coroutine_consumer_queue_with_priority(priority_queue, event),
             simple_coroutine_feeder_queue_with_priority(priority_queue, event)]
    await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())
