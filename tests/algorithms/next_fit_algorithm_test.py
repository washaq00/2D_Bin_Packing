import pytest

from data_operations.data_operations import DataOperations
from data_operations.data_generator import OnlineGenerator
from algorithms.next_fit_algorithm import NextFitAlgorithm
from ploting import plot_bins2d

WITH_PRINT = False
WITH_BLOCK = False


def test_if_create_3_bins_for_literature_example():
    gen = OnlineGenerator(DataOperations().load_from_file('tests/data/test1.in'))
    alg = NextFitAlgorithm(gen.bin_width, gen.bin_height, gen)

    assert alg.run() == 3
    assert alg.is_valid()

    if WITH_PRINT:
        plot_bins2d(alg.closed_bins, block=WITH_BLOCK)

