from random import randint

from sensors.generators.generator import Generator


class RandomGenerator(Generator):
    def generate(self) -> int:
        return randint(-32768, 32767)
