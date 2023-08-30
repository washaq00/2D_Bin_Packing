from algorithms.algorithm_base import OnlineAlgorithm
from data_operations.data_generator import GeneratorBaseType
from data_structures.bin_2d import Bin2D
from data_structures.package_2d import Package2D
from data_structures.point_2d import Point2D
from dataclasses import dataclass, field
from typing import List, Tuple
from collections import deque
from data_structures.rectangle import Rectangle


"""
Base class for algorithms
"""


@dataclass
class Skyline:
    points: List[Point2D]  # list of bottom left points


@dataclass
class OpenedBin:
    bin: Bin2D
    skyline: List[Point2D]  # list of bottom left points from top view of bin (skyline)
    waste_map: List[Rectangle]  # closed rectangles spaces


class SkylineBestFitAlgorithm(OnlineAlgorithm):
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

    def _get_left_width_for_fit(self, opened_bin: OpenedBin, loc: Point2D, package: Package2D) -> int | None:
        top_height = opened_bin.bin.height
        for level in reversed(opened_bin.levels):
            if level[1] > loc.y:
                top_height = level[1]
            else:
                break

        if self._check_if_fit(loc, top_height, package):
            return self.bin_width - loc.x + package.width
        return None

    def _open_bin(self):
        self.opened_bins.append(OpenedBin(Bin2D(self.bin_width, self.bin_height), [Point2D(0, 0)], []))

    def _close_all(self) -> None:
        for i in self.opened_bins:
            self.closed_bins.append(i.bin)
        self.opened_bins.clear()

    @staticmethod
    def _pack_in_best_loc(best_loc: Tuple[OpenedBin, Point2D, int], package: Package2D) -> None:
        opened_bin, loc, level_idx = best_loc
        opened_bin.bin.insert(loc, package)

        if loc.x == 0 and loc.y + package.height < opened_bin.bin.height:
            # if beginning of row, create new one above
            opened_bin.levels.append([0, loc.y + package.height])
        opened_bin.levels[level_idx][0] += package.width

    def _pack(self, package: Package2D) -> None:
        best_loc: (OpenedBin, Point2D, int) = None
        width_left_for_best_loc: int | None = None

        for ob in self.opened_bins:  # loop over all levels of all bins
            for level_idx in range(len(ob.levels)):
                width, height = ob.levels[level_idx]
                left_width = self._get_left_width_for_fit(ob, Point2D(width, height), package)

                if left_width is not None:
                    if left_width == 0:  # package left no free space on this level, so it is just best choice
                        best_loc = (ob, Point2D(width, height), level_idx)
                        self._pack_in_best_loc(best_loc, package)
                        return
                    elif width_left_for_best_loc is None:  # empty best_loc, first search and assign
                        width_left_for_best_loc = left_width
                        best_loc = (ob, Point2D(width, height), level_idx)
                    elif width_left_for_best_loc > left_width:  # found space with less loss
                        width_left_for_best_loc = left_width
                        best_loc = (ob, Point2D(width, height), level_idx)

        if width_left_for_best_loc is not None:  # best package found with minimal lose
            self._pack_in_best_loc(best_loc, package)
            return

        # if no free space in other boxes, create new
        self._open_bin()
        width, height = self.opened_bins[-1].levels[0]
        if self._insert_if_fit(self.opened_bins[-1], Point2D(width, height), package):
            if height + package.height < self.opened_bins[-1].bin.height:
                # if new level can be added, create new one above
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
