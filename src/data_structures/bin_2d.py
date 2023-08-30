import itertools
from data_structures.package_2d import Package2D, PlacedPackage2D
from data_structures.point_2d import Point2D
from data_structures.rectangle import Rectangle
from typing import List


class Bin2D(Rectangle):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.packages: List[PlacedPackage2D] = []

    def __str__(self):
        temp = ""
        for package in self.packages:
            temp += f"{package.__str__()}, "
        return f"size: {self.width}x{self.height} packages: [{temp[:-2]}]"

    def is_empty(self) -> bool:
        return False if len(self.packages) else True

    def insert(self, location: Point2D, package: Package2D) -> None:
        self.packages.append(PlacedPackage2D.from_package(package, location))

    @staticmethod
    def _is_intersect(first: PlacedPackage2D, second: PlacedPackage2D):
        if (
            first.location.x >= second.location.x + second.width
            or first.location.x + first.width <= second.location.x
            or first.location.y + first.height >= second.location.y
            or first.location.y <= second.location.y + second.height
        ):
            return False

        return True

    @staticmethod
    def _is_contains(outer: PlacedPackage2D, inner: PlacedPackage2D):
        if (
            inner.location.x >= outer.location.x
            and inner.location.y >= outer.location.y
            and inner.location.x + inner.width <= outer.location.x + outer.width
            and inner.location.y + inner.height <= outer.location.y + outer.height
        ):
            return True

        return False

    def is_valid(self) -> bool:
        box = PlacedPackage2D(self.width, self.height, Point2D(0, 0))
        for el in self.packages:
            if not self._is_contains(box, el):
                return False

        for el1, el2 in itertools.combinations(self.packages, 2):
            if self._is_intersect(el1, el2) or self._is_contains(el1, el2) or self._is_contains(el2, el1):
                return False
        return True
