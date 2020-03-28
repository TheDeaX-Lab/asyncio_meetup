import asyncio
import uvloop

uvloop.install()


async def handle_echo(reader, writer):
    while True:
        data = await reader.read(100)
        if len(data):
            message = data.decode()
            addr = writer.get_extra_info('peername')
            print(f"Received {message} from {addr}")
            print(f"Send: {message}")
            writer.write(data)
            await writer.drain()
        else:
            print('Close the connection')
            writer.close()
            break


async def main():
    server = await asyncio.start_server(handle_echo, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
