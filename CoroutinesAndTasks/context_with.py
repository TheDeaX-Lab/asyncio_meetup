import asyncio
import uvloop

try:
    from contextlib import asynccontextmanager
except ImportError:
    from async_generator import asynccontextmanager

uvloop.install()


# as function
@asynccontextmanager
async def simple_context_coroutine(a):
    # before yield __aenter__, after yield __aexit__
    await asyncio.sleep(1)
    try:
        yield a
    finally:
        await asyncio.sleep(1)
        print("Context exited!")


# as class
class SimpleContext:
    def __init__(self, a):
        self.value = a

    async def __aenter__(self):
        await asyncio.sleep(1)
        return self.value

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await asyncio.sleep(1)
        print("Context exited!")


# as class without context manager
class WithoutWith:
    def __init__(self, a):
        self.value = a

    async def enter(self):
        await asyncio.sleep(1)
        return self.value

    async def exit(self):
        await asyncio.sleep(1)
        print("Context completed!")


async def main():
    async with simple_context_coroutine(1) as value:
        print(value)
    async with SimpleContext(2) as value:
        print(value)

    # Equivalent to
    obj = WithoutWith(3)
    try:
        value = await obj.enter()
        print(value)
    finally:
        await obj.exit()
        del obj


if __name__ == '__main__':
    asyncio.run(main())
