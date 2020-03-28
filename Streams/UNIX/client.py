import asyncio
import uvloop
import sys

uvloop.install()


async def main():
    path = sys.argv[1]
    reader, writer = await asyncio.open_unix_connection(path)
    print(f"Connected with addr: {path}")
    while True:
        try:
            text = input(f"{path}>")
            if len(text):
                writer.write(text.encode())
                await writer.drain()
                text = await reader.read(100)
                print(text.decode())
        except KeyboardInterrupt:
            writer.close()
            print()
            print("Client closed")
            break


if __name__ == '__main__':
    asyncio.run(main())
