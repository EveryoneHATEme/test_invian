from random import randint

from sensors.generators.generator import Generator


class RandomGenerator(Generator):
    """
    Example of generator
    Generates random numbers in range from -32768 to 32767 (or 2-byte integer range)
    """

    def generate(self) -> int:
        return randint(-32768, 32767)
