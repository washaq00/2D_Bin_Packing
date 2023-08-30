import pytest

from src.data_structures.bin_2d import *
from src.data_structures.package_2d import *
from src.data_structures.point_2d import *


def test_insert_package_in_box():
    bin = Bin2D(10, 6)
    assert bin.is_empty()
    assert bin.is_valid()

    bin.insert(Point2D(0, 0), Package2D(4, 4))
    assert not bin.is_empty()
    assert bin.is_valid()


def test_insert_package_same_size_as_box():
    bin = Bin2D(10, 6)
    assert bin.is_empty()
    assert bin.is_valid()

    bin.insert(Point2D(0, 0), Package2D(10, 6))
    assert not bin.is_empty()
    assert bin.is_valid()


def test_insert_multi_packages_in_box():
    bin = Bin2D(10, 10)
    assert bin.is_empty()
    assert bin.is_valid()

    for i in range(10):
        for j in range(10):
            bin.insert(Point2D(i, j), Package2D(1, 1))
            assert bin.is_valid()


def test_insert_two_packages_of_same_size():
    bin = Bin2D(10, 5)
    assert bin.is_empty()
    assert bin.is_valid()

    bin.insert(Point2D(0, 0), Package2D(5, 5))
    assert not bin.is_empty()
    assert bin.is_valid()

    bin.insert(Point2D(5, 0), Package2D(5, 5))
    assert bin.is_valid()

    bin.insert(Point2D(5, 0), Package2D(5, 5))
    assert not bin.is_valid()
