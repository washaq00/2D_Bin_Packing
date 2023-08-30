import pytest

from data_operations.data_operations import DataOperations
from data_operations.data_generator import OnlineGenerator
from algorithms.best_long_side_first import BestLongSideFitAlgorithm
from ploting import plot_bins2d

WITH_PRINT = True
WITH_BLOCK = True


def test_if_create_3_bins_for_literature_example():
    gen = OnlineGenerator(DataOperations().load_from_file('tests/data/test1.in'))
    alg = BestLongSideFitAlgorithm(gen.bin_width, gen.bin_height, gen)

    test = alg.run()
    assert alg.is_valid()

    if WITH_PRINT:
        plot_bins2d(alg.closed_bins, block=WITH_BLOCK)

