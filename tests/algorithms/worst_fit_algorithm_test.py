import pytest

from data_operations.data_operations import DataOperations
from data_operations.data_generator import OnlineGenerator
from algorithms.worst_fit_algorithm import WorstFitAlgorithm
from ploting import plot_bins2d

WITH_PRINT = True
WITH_BLOCK = True


def test_if_create_2_bins_for_literature_example():
    gen = OnlineGenerator(DataOperations().load_from_file('tests/data/test1.in'))
    alg = WorstFitAlgorithm(gen.bin_width, gen.bin_height, gen)

    assert alg.run() == 2
    assert alg.is_valid()

    if WITH_PRINT:
        plot_bins2d(alg.closed_bins, block=WITH_BLOCK)

