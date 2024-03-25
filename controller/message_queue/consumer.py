import struct
from datetime import datetime
from collections import namedtuple

import aio_pika

from controller.message_queue.amqp import AMQP
from common.config import config

Message = namedtuple("Message", ["timestamp", "payload"])


class Consumer(AMQP):
    async def get_last_messages(self) -> list[Message[int, int]]:
        messages = []

        call_timestamp = datetime.utcnow().timestamp()

        await self.queue.declare()
        messages_count = self.queue.declaration_result.message_count

        for i in range(messages_count):
            message = await self.queue.get(no_ack=True, fail=False)

            if message is None:
                break

            async with message.process(ignore_processed=True):
                message_unpacked = self.unpack_message(message)

                if (
                    call_timestamp - message_unpacked.timestamp
                    < config.MANIPULATOR_UPDATE_TIME
                ):
                    messages.append(message_unpacked)

            if (
                datetime.utcnow().timestamp() - call_timestamp
                >= config.MANIPULATOR_UPDATE_TIME
            ):
                break

        return messages

    @staticmethod
    def unpack_message(
        message: aio_pika.abc.AbstractIncomingMessage,
    ) -> Message[int, int]:
        return Message(*struct.unpack(">2i", message.body))
