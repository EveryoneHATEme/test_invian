import asyncio
from asyncio import StreamReader, StreamWriter

from common.config import config


class TCPServer:
    def __init__(
        self, server_ip=config.CONTROLLER_IP, port=config.CONTROLLER_TCP_PORT
    ) -> None:
        self.server_ip = server_ip
        self.port = port
        self.writer: StreamWriter | None = None
        self.server = None
        self.server_task: asyncio.Task | None = None

    async def start(self) -> None:
        self.server_task = asyncio.create_task(self.start_server_and_serving())

    async def stop(self) -> None:
        if self.writer is not None:
            self.writer.close()
            await self.writer.wait_closed()
        if self.server_task is not None:
            self.server_task.cancel()

    async def start_server_and_serving(self):
        self.server = await asyncio.start_server(
            self.handle_client, host=self.server_ip, port=self.port
        )
        async with self.server:
            await self.server.serve_forever()

    async def handle_client(self, reader: StreamReader, writer: StreamWriter) -> None:
        if self.writer is None:
            self.writer = writer

    async def send_message(self, message: str) -> None:
        self.writer.write(message.encode())
        await self.writer.drain()
        await asyncio.sleep(0)
