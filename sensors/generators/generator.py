from abc import ABC, abstractmethod
from random import randint


class Generator(ABC):
    @abstractmethod
    def generate(self) -> int:
        pass


class RandomGenerator(Generator):
    def generate(self) -> int:
        return randint(-32768, 32767)
