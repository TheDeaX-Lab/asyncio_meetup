import asyncio
import uvloop

uvloop.install()


async def simple_generator_coroutine(a):
    for i in range(5):
        yield i
    print(f"Completed {a}")


async def simple_generator_with_accept_data(a):
    while 1:
        b = yield a
        print(b)
        if b:
            break
        print("Go again")
    print(f"Completed {a}")


async def main():
    gen = simple_generator_with_accept_data(1)
    # Start generator
    data = await gen.asend(None)
    print(data)

    data = await gen.asend([])
    print(data)
    data = await gen.asend(set())
    print(data)
    data = await gen.asend(None)
    try:
        await gen.asend(True)
    except StopAsyncIteration as e:
        ...

    async for value in simple_generator_coroutine(1):
        print(value)

    # Equivalent to
    gen = simple_generator_coroutine(1)
    while True:
        try:
            value = await gen.__anext__()
            # Equivalent to
            # value = await gen.asend(None)
        except StopAsyncIteration:
            break
        print(value)


if __name__ == '__main__':
    asyncio.run(main())
