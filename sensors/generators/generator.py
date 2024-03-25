from abc import ABC, abstractmethod


class Generator(ABC):
    """
    Abstract class for generating data.
    To create a generator, inherit this class and override the generate method
    """

    @abstractmethod
    def generate(self) -> int:
        pass
