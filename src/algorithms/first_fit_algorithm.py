from algorithms.algorithm_base import OnlineAlgorithm
from data_operations.data_generator import GeneratorBaseType
from data_structures.bin_2d import Bin2D
from data_structures.package_2d import Package2D
from data_structures.point_2d import Point2D
from collections import deque
from dataclasses import dataclass, field
from typing import List

"""
Base class for algorithms
"""


@dataclass
class OpenedBin:
    bin: Bin2D
    levels: List[List[int]] = field(default_factory=list)  # available levels for bin list([width, height])


class FirstFitAlgorithm(OnlineAlgorithm):
    def __init__(self, bin_width: int, bin_height: int, generator: GeneratorBaseType):
        super().__init__(bin_width, bin_height, generator)
        self.opened_bins: deque[OpenedBin] = deque()  # type: ignore
        self._open_bin()

    def _check_if_fit(self, loc: Point2D, top_height: int, package: Package2D):
        if loc.x + package.width > self.bin_width or loc.y + package.height > top_height:
            return False
        return True

    def _insert_if_fit(self, opened_bin: OpenedBin, loc: Point2D, package: Package2D):
        top_height = opened_bin.bin.height
        for level in reversed(opened_bin.levels):
            if level[1] > loc.y:
                top_height = level[1]
            else:
                break

        if self._check_if_fit(loc, top_height, package):
            opened_bin.bin.insert(loc, package)
            return True
        return False

    def _open_bin(self):
        self.opened_bins.append(OpenedBin(Bin2D(self.bin_width, self.bin_height), [[0, 0]]))

    def _close_all(self) -> None:
        for i in self.opened_bins:
            self.closed_bins.append(i.bin)
        self.opened_bins.clear()

    def _pack(self, package: Package2D) -> None:
        for ob in self.opened_bins:
            for i in range(len(ob.levels)):
                width, height = ob.levels[i]
                if self._insert_if_fit(ob, Point2D(width, height), package):
                    if width == 0 and height + package.height < ob.bin.height:
                        # if beginning of row, create new one above
                        ob.levels.append([0, height + package.height])
                    ob.levels[i][0] += package.width

                    return

        # if no free space in other boxes, create new
        self._open_bin()
        width, height = self.opened_bins[-1].levels[0]
        if self._insert_if_fit(self.opened_bins[-1], Point2D(width, height), package):
            if width == 0 and height + package.height < self.opened_bins[-1].bin.height:
                # if beginning of row, create new one above
                self.opened_bins[-1].levels.append([0, height + package.height])
            self.opened_bins[-1].levels[0][0] += package.width

            return

        RuntimeError("Package bigger than bin")

    def run(self) -> int:
        while True:
            package = self.data_generator.get()
            if package is None:
                break
            self._pack(package)

        self._close_all()
        return len(self.closed_bins)
