import json
from time import time

import aio_pika

from controller.message_queue.amqp import AMQP
from controller.models import SensorDataModel
from common.config import config


class Producer(AMQP):
    async def add_sensor_message(self, sensor_data: SensorDataModel) -> None:
        message_body = {**sensor_data.model_dump(), "time": time()}
        await self.exchange.publish(
            aio_pika.Message(body=json.dumps(message_body).encode()),
            routing_key=config.RABBITMQ_QUEUE,
        )
