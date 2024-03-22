from datetime import datetime

import requests

from generator import Generator, RandomGenerator


class Sensor:
    def __init__(self,
                 controller_address: str,
                 data_generator_cls: type[Generator] = RandomGenerator,
                 timeout: float = 1. / 300) -> None:
        self.data_generator = data_generator_cls()

        self.controller_address = controller_address
        self.session = requests.Session()
        self.payload = {'datetime': '', 'payload': 0}
        self.timeout = timeout

    def __del__(self) -> None:
        self.session.close()

    def send(self, payload: int) -> None:
        self.payload['datetime'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        self.payload['payload'] = payload

        self.session.post(url=self.controller_address, json=self.payload, timeout=self.timeout)

    def start(self) -> None:
        self.loop()

    def loop(self) -> None:
        while True:
            read_data = self.data_generator.generate()
            self.send(read_data)
