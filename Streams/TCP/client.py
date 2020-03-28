import asyncio
import uvloop
import sys

uvloop.install()


async def main():
    host, port = sys.argv[1:3]
    reader, writer = await asyncio.open_connection(host, port)
    addr = writer.get_extra_info("peername")
    print(f"Connected with addr: {addr}")
    while True:
        try:
            text = input(f"{host}:{port}>")
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
