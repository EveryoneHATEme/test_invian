from multiprocessing import Process
from time import sleep

from sensors.sensor import Sensor


class SensorsManager:
    def __init__(self,
                 number_of_sensors: int = 8,
                 sensor_request_timeout: float = 1. / 300,
                 controller_address: str = 'http://127.0.0.1:8000') -> None:
        self.sensor_request_timeout = sensor_request_timeout
        self.controller_address = controller_address

        self.sensors = [
            Sensor(self.controller_address, timeout=self.sensor_request_timeout) for _ in range(number_of_sensors)
        ]
        self.processes = [Process(target=sensor.start()) for sensor in self.sensors]

    def start(self) -> None:
        for process in self.processes:
            process.start()
        print('started')

    def __delete__(self) -> None:
        for sensor, process in zip(self.sensors, self.processes):
            del sensor
            process.join()


def launch() -> None:
    manager = SensorsManager()
    manager.start()


if __name__ == '__main__':
    launch()
