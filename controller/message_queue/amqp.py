import aio_pika
from common.config import config


class AMQP:
    def __init__(self):
        self.connection: aio_pika.abc.AbstractRobustConnection | None = None
        self.channel: aio_pika.abc.AbstractChannel | None = None
        self.exchange: aio_pika.abc.AbstractExchange | None = None
        self.queue: aio_pika.abc.AbstractQueue | None = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(config.RABBITMQ_URL, timeout=240)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)
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
