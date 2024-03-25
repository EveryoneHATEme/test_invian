import asyncio
from datetime import datetime
import struct

import aio_pika

from controller.message_queue.amqp import AMQP
from controller.models import SensorDataModel
from common.config import config


class Producer(AMQP):
    def __init__(self, batch_size: int = 128) -> None:
        AMQP.__init__(self)
        self.outstanding_messages = []
        self.batch_size = batch_size

    async def add_sensor_message(self, sensor_data: SensorDataModel) -> None:
        message_body = struct.pack(
            ">2i",
            int(
                datetime.strptime(sensor_data.datetime, "%Y-%m-%dT%H:%M:%S").timestamp()
            ),
            sensor_data.payload,
        )

        self.outstanding_messages.append(
            asyncio.create_task(
                self.exchange.publish(
                    aio_pika.Message(
                        body=message_body,
                        expiration=config.MANIPULATOR_UPDATE_TIME * 1000,
                    ),
                    routing_key=config.RABBITMQ_QUEUE,
                )
            )
        )
        await asyncio.sleep(0)
        await self.send_batch()

    async def send_batch(self) -> None:
        if len(self.outstanding_messages) >= self.batch_size:
            await asyncio.gather(*self.outstanding_messages)
            self.outstanding_messages.clear()
