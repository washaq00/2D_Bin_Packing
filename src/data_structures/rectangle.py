from data_structures.point_2d import Point2D
from typing import TypeVar


class Rectangle:
    T = TypeVar("T", bound="Rectangle")

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class PlacedRectangle(Rectangle):
    def __init__(self, width: int, height: int, location: Point2D):
        super().__init__(width, height)
        self.location = location

    def __str__(self):
        return f"{self.width}x{self.height} loc: {self.location}"

    @classmethod
    def from_rectangle(cls, rectangle: Rectangle, location: Point2D):
        return cls(rectangle.width, rectangle.height, location)
