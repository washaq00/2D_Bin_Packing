from algorithms.algorithm_base import OnlineAlgorithm
from data_operations.data_generator import GeneratorBaseType
from data_structures.bin_2d import Bin2D
from data_structures.package_2d import Package2D
from data_structures.point_2d import Point2D
from typing import List

"""
Base class for algorithms
"""


class NextFitAlgorithm(OnlineAlgorithm):
    def __init__(self, bin_width: int, bin_height: int, generator: GeneratorBaseType):
        super().__init__(bin_width, bin_height, generator)
        self.opened_bins: List[Bin2D] = []
        self._current_height = 0
        self._current_width = 0
        self._next_height = 0
        self._open_bin()

    def _check_if_fit(self, loc: Point2D, package: Package2D):
        if loc.x + package.width > self.bin_width or loc.y + package.height > self.bin_height:
            return False
        return True

    def _insert_if_fit(self, loc: Point2D, package: Package2D):
        if self._check_if_fit(loc, package):
            self.opened_bins[0].insert(loc, package)
            return True
        return False

    def _open_bin(self):
        self.opened_bins.append(Bin2D(self.bin_width, self.bin_height))
        self._current_height = 0
        self._current_width = 0
        self._next_height = 0

    def _pack(self, package: Package2D) -> None:
        if self._insert_if_fit(
            Point2D(self._current_width, self._current_height), package
        ):  # insert first package or another in same row
            self._current_width = self._current_width + package.width
            if (
                self._next_height < self._current_height + package.height
            ):  # next_height is on level of current row the highest package
                self._next_height = self._current_height + package.height
        elif self._insert_if_fit(Point2D(0, self._next_height), package):  # insert package in new row
            self._current_height = self._next_height
            self._current_width = package.width
            self._next_height += package.height
        else:  # open new bin
            self.closed_bins.append(self.opened_bins.pop(0))
            self._open_bin()
            if self._insert_if_fit(Point2D(self._current_width, self._current_height), package):
                self._current_width = package.width
                self._next_height = package.height
            else:
                RuntimeError("Package bigger than bin")

    def run(self) -> int:
        while True:
            package = self.data_generator.get()
            if package is None:
                break
            self._pack(package)

        self._close_all()
        return len(self.closed_bins)
