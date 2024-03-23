import json
import pprint

from common.tcp_client import TCPClient


class Manipulator:
    def __init__(self):
        self.client = TCPClient()

    async def listen_commands(self):
        await self.client.connect()
        async for command in self.client.receive_messages():
            parsed_command = json.loads(command)
            self.do_action(parsed_command)

        await self.client.disconnect()

    @staticmethod
    def do_action(command: dict[str, str]):
        print(f"Received command: {pprint.pformat(command, indent=4)}")
