from algorithms.algorithm_base import OnlineAlgorithm
from data_operations.data_generator import GeneratorBaseType
from data_structures.bin_2d import Bin2D
from data_structures.package_2d import Package2D
from data_structures.point_2d import Point2D
from dataclasses import dataclass, field
from typing import List, Tuple
from collections import deque

"""
Base class for algorithms
"""


@dataclass
class OpenedBin:
    bin: Bin2D
    levels: List[List[int]] = field(default_factory=list)  # available levels for bin list((width, height))


class BestLongSideFitAlgorithm(OnlineAlgorithm):
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
        best_bin = None
        best_level = None
        best_long_side = float('inf')

        for ob in self.opened_bins:
            for i in range(len(ob.levels)):
                width, height = ob.levels[i]
                long_side = max(ob.bin.width - width, ob.bin.height - height)
                free_space_area = long_side * min(ob.bin.width - width, ob.bin.height - height)
                if self._check_if_fit(Point2D(width, height), ob.bin.height, package) and free_space_area < best_long_side:
                    best_bin = ob
                    best_level = i
                    best_long_side = free_space_area

        if best_bin is not None:
            width, height = best_bin.levels[best_level]
            assert self._check_if_fit(Point2D(width, height), best_bin.bin.height, package)
            assert self._insert_if_fit(best_bin, Point2D(width, height), package)
            best_bin.levels[best_level][0] += package.width

            if best_bin.levels[best_level][0] == best_bin.bin.width:
                best_bin.levels.pop(best_level)

            return

        # if no free space in other bins, create new
        self._open_bin()
        width, height = self.opened_bins[-1].levels[0]
        if self._insert_if_fit(self.opened_bins[-1], Point2D(width, height), package):
            if height + package.height < self.opened_bins[-1].bin.height:
                self.opened_bins[-1].levels.append([0, height + package.height])
            self.opened_bins[-1].levels[0][0] += package.width

            return

        raise RuntimeError("Package bigger than bin")

    def run(self) -> int:
        while True:
            package = self.data_generator.get()
            if package is None:
                break
            self._pack(package)

        self._close_all()
        return len(self.closed_bins)
