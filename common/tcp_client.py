import asyncio
from asyncio import StreamReader, StreamWriter
from typing import Generator

from common.config import config


class TCPClient:
    def __init__(
        self,
        host_ip: str = config.CONTROLLER_IP,
        port: int = config.CONTROLLER_TCP_PORT,
    ) -> None:
        self.host_ip = host_ip
        self.port = port
        self.reader: StreamReader | None = None
        self.writer: StreamWriter | None = None

    async def connect(self) -> None:
        self.reader, self.writer = await asyncio.open_connection(
            'controller', self.port
        )

    async def disconnect(self) -> None:
        self.writer.close()
        await self.writer.wait_closed()

    async def receive_messages(self) -> Generator[bytes, None, None]:
        try:
            while True:
                message = await self.reader.read(1024)
                if not message:
                    print('no messages')
                    break
                yield message.decode()
        except asyncio.CancelledError:
            await self.disconnect()
