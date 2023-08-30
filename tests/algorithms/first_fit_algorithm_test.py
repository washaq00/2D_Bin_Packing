import pytest

from data_operations.data_operations import DataOperations
from data_operations.data_generator import OnlineGenerator
from algorithms.first_fit_algorithm import FirstFitAlgorithm
from ploting import plot_bins2d
import pprint

WITH_PRINT = True
WITH_BLOCK = True


def test_if_create_2_bins_for_literature_example():
    gen = OnlineGenerator(DataOperations().load_from_file('tests/data/test1.in'))
    alg = FirstFitAlgorithm(gen.bin_width, gen.bin_height, gen)

    alg.run()

    for i in alg.closed_bins:
        print(i)

    assert alg.run() == 2
    assert alg.is_valid()

    if WITH_PRINT:
        plot_bins2d(alg.closed_bins, block=WITH_BLOCK)

