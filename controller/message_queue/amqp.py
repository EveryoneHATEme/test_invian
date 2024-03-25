import asyncio

import aio_pika
from common.config import config


class AMQP:
    """
    Inherited class for producer and consumer that implements the connection to RabbitMQ
    """

    def __init__(self):
        self.connection: aio_pika.abc.AbstractRobustConnection | None = None
        self.channel: aio_pika.abc.AbstractChannel | None = None
        self.exchange: aio_pika.abc.AbstractExchange | None = None
        self.queue: aio_pika.abc.AbstractQueue | None = None

    async def connect(self):
        while True:
            try:
                self.connection = await aio_pika.connect_robust(
                    config.RABBITMQ_URL, timeout=240
                )
            except aio_pika.exceptions.AMQPConnectionError:
                await asyncio.sleep(1)
            else:
                break
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            config.RABBITMQ_EXCHANGE, aio_pika.ExchangeType.DIRECT, durable=True
        )
        self.queue = await self.channel.declare_queue(
            config.RABBITMQ_QUEUE, durable=True
        )
        await self.queue.bind(self.exchange, config.RABBITMQ_QUEUE)

    async def disconnect(self):
        await self.channel.close()
        await self.connection.close()
