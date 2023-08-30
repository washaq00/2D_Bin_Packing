from os.path import join, isfile, isdir
from algorithms.algorithm_base import AlgorithmBase
from data_operations.data_operations import DataOperations
from packing_stats import PackingResult, PackingStats
from typing import Type, cast, Dict, List, Tuple
from data_structures.bin_2d import Bin2D


def run_algorithm(
    path: str, algorithm: Type[AlgorithmBase], with_validation=True
) -> Tuple[PackingStats | PackingResult | int, List[Bin2D] | List[List[Bin2D]]]:
    if isfile(path):
        print(f"Running for file {path}")
        return run_for_file(path, algorithm, with_validation)
    elif isdir(path):
        print(f"Running for directory {path}")
        return run_for_directory(path, algorithm, with_validation)
    else:
        raise RuntimeError(f"Not file or directory: {path}")


def print_result(path: str, algorithm: Type[AlgorithmBase], res: PackingStats | PackingResult | int):
    if isinstance(res, PackingStats):
        print(f"Result for {path}:")
        res.print_results_for_algorithm(algorithm.__name__)
    elif isinstance(res, PackingResult):
        print(f"Result for {path} and {algorithm.__name__}: {res}")
    elif isinstance(res, int):
        print(f"Result for {path} and {algorithm.__name__}: {res} bins")
    else:
        RuntimeError(f"Wrong type: {type(res)}")


def plot_results(path: str, algorithm: Type[AlgorithmBase], res: PackingStats | PackingResult | int):
    if isinstance(res, PackingStats):
        print(f"Result for {path}:")
        res.print_results_for_algorithm(algorithm.__name__)
    elif isinstance(res, PackingResult):
        print(f"Result for {path} and {algorithm.__name__}: {res}")
    elif isinstance(res, int):
        print(f"Result for {path} and {algorithm.__name__}: {res} bins")
    else:
        RuntimeError(f"Wrong type: {type(res)}")


def run_for_file(
    file: str, algorithm: Type[AlgorithmBase], with_validation=True
) -> Tuple[PackingResult | int, List[Bin2D]]:
    gen = algorithm.get_generator()(DataOperations().load_from_file(file))
    alg = algorithm(gen.bin_width, gen.bin_height, gen)
    bins_num = alg.run()

    if with_validation and not alg.is_valid():
        RuntimeError(f"Invalid result for {algorithm.__name__} file {file}")

    parsed = DataOperations().parse_input_file_name(file)
    if parsed is None:
        return bins_num, alg.closed_bins
    else:
        return (
            PackingResult(
                bins_num,
                parsed["size"],
                parsed["max_width"],
                parsed["max_height"],
                parsed["box_width"],
                parsed["box_height"],
            ),
            alg.closed_bins,
        )


def run_for_directory(
    directory: str, algorithm: Type[AlgorithmBase], with_validation=True
) -> Tuple[PackingStats, List[List[Bin2D]]]:
    do = DataOperations()
    stats = PackingStats()
    files = do.get_all_input_files(directory)
    files.sort(key=str.upper)
    bins_list = []

    for f in files:
        gen = algorithm.get_generator()(DataOperations().load_from_file(join(directory, f)))
        alg = algorithm(gen.bin_width, gen.bin_height, gen)
        bins_num = alg.run()
        bins_list.append(alg.closed_bins)

        if with_validation and not alg.is_valid():
            RuntimeError(f"Invalid result for {algorithm.__name__} file {f}")

        parsed = do.parse_input_file_name(f)
        if parsed is None:
            RuntimeError("Invalid input file name")
        parsed = cast(Dict[str, int], parsed)
        res = PackingResult(
            bins_num,
            parsed["size"],
            parsed["max_width"],
            parsed["max_height"],
            parsed["box_width"],
            parsed["box_height"],
        )
        stats.add_result(algorithm.__name__, res)

    return stats, bins_list
