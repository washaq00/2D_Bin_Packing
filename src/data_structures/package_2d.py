from data_structures.point_2d import Point2D
from typing import TypeVar
from data_structures.rectangle import Rectangle, PlacedRectangle


class Package2D(Rectangle):
    T = TypeVar("T", bound="Package2D")

    def __init__(self, width: int, height: int, id=0):
        super().__init__(width, height)
        self.id = id


class PlacedPackage2D(Package2D):
    def __init__(self, width: int, height: int, location: Point2D, id=0):
        super().__init__(width, height, id)
        self.location = location

    def __str__(self):
        return f"id: {self.id} size: {self.width}x{self.height} loc: {self.location}"

    @classmethod
    def from_package(cls, package: Package2D, location: Point2D):
        return cls(package.width, package.height, location, package.id)
