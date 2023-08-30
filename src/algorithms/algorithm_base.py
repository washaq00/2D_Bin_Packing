from abc import ABC, abstractmethod
from data_structures.bin_2d import Bin2D
from data_operations.data_generator import OnlineGenerator, OfflineGenerator, GeneratorBaseType
from typing import List, Type

"""
Base class for algorithms
"""


class AlgorithmBase(ABC):
    def __init__(self, bin_width: int, bin_height: int, generator: GeneratorBaseType):
        self.data_generator = generator
        self.bin_width = bin_width
        self.bin_height = bin_height
        self.opened_bins: List[Bin2D] = []
        self.closed_bins: List[Bin2D] = []
        super().__init__()

    @abstractmethod
    def run(self):
        RuntimeError("Not implemented")

    def is_valid(self) -> bool:
        for bin in self.closed_bins:
            if not bin.is_valid():
                return False
        return True

    def _close_all(self) -> None:
        for i in self.opened_bins:
            self.closed_bins.append(i)
        self.opened_bins.clear()

    @staticmethod
    @abstractmethod
    def get_generator():
        RuntimeError("Not implemented")


class OnlineAlgorithm(AlgorithmBase):
    def __init__(self, bin_width: int, bin_height: int, generator: GeneratorBaseType):
        super().__init__(bin_width, bin_height, generator)
        if not isinstance(self.data_generator, OnlineGenerator):
            RuntimeError(f"Wrong generator type. Expected {OnlineGenerator}, get {generator}")

    @abstractmethod
    def run(self):
        RuntimeError("Not implemented")

    @staticmethod
    def get_generator() -> Type[OnlineGenerator]:
        return OnlineGenerator


class OfflineAlgorithm(AlgorithmBase):
    def __init__(self, bin_width: int, bin_height: int, generator: GeneratorBaseType):
        super().__init__(bin_width, bin_height, generator)
        if not isinstance(self.data_generator, OfflineGenerator):
            RuntimeError(f"Wrong generator type. Expected {OfflineGenerator}, get {generator}")

    @abstractmethod
    def run(self):
        RuntimeError("Not implemented")

    @staticmethod
    def get_generator() -> Type[OfflineGenerator]:
        return OfflineGenerator
