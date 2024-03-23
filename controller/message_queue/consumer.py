import json

import aio_pika

from controller.message_queue.amqp import AMQP
from common.config import config


class Consumer(AMQP):
    async def get_last_messages(self) -> list[dict[str, str | int | float]]:
        messages = []
        start_time = 0
        async with self.queue.iterator() as queue_iterator:
            async for msg in queue_iterator:
                processed_msg = await self.process_message(msg)
                messages.append(
                    {
                        "datetime": processed_msg["datetime"],
                        "payload": processed_msg["payload"],
                    }
                )
                if not start_time:
                    start_time = processed_msg["time"]
                if processed_msg["time"] - start_time >= config.MANIPULATOR_WAIT_TIME:
                    break

        return messages

    @staticmethod
    async def process_message(
        message: aio_pika.IncomingMessage,
    ) -> dict[str, str | int | float]:
        async with message.process():
            return json.loads(message.body.decode())
