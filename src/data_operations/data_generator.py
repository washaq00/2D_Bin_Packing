from abc import ABC, abstractmethod
import pandas
from data_structures.package_2d import Package2D
from typing import List, TypeVar


class GeneratorBase(ABC):
    def __init__(self, df: pandas.DataFrame):
        input_values: list = df.values.tolist()

        self.packages: List[Package2D] = []
        self.bin_width, self.bin_height = input_values.pop(0)
        super().__init__()

        for i in range(len(input_values)):
            width, height = input_values[i]
            self.packages.append(Package2D(width, height, i + 1))

    @abstractmethod
    def get(self):
        RuntimeError("Not implemented")


GeneratorBaseType = TypeVar("GeneratorBaseType", bound=GeneratorBase)


class OnlineGenerator(GeneratorBase):
    def __init__(self, df: pandas.DataFrame):
        super().__init__(df)

    def get(self) -> Package2D | None:
        if len(self.packages):
            return self.packages.pop(0)
        else:
            return None


class OfflineGenerator(GeneratorBase):
    def __init__(self, df: pandas.DataFrame):
        super().__init__(df)

    def get(self) -> List[Package2D]:
        return self.packages
