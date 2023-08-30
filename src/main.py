import argparse
from algorithms_launcher import run_algorithm, print_result
from algorithms.next_fit_algorithm import NextFitAlgorithm
from algorithms.best_fit_algorithm import BestFitAlgorithm
from algorithms.first_fit_algorithm import FirstFitAlgorithm
from algorithms.worst_fit_algorithm import WorstFitAlgorithm
from algorithms.best_short_side_first import BestShortSideFitAlgorithm
from algorithms.best_long_side_first import BestLongSideFitAlgorithm
from typing import Optional, Sequence

__version__ = "1.0.0"

alg_collection = {
    "next_fit": NextFitAlgorithm,
    "first_fit": FirstFitAlgorithm,
    "best_fit": BestFitAlgorithm,
    "worst_fit": WorstFitAlgorithm,
    "best_short_side_first": BestShortSideFitAlgorithm,
    "best_long_side_first": BestLongSideFitAlgorithm,
}


def main(parameters: Optional[Sequence[str]] = None):
    parser = argparse.ArgumentParser()
    parser.set_defaults(action=run)
    parser.add_argument("-v", "--version", action="version", version=f"bin_packing_2d {__version__}")
    parser.add_argument(
        "-i", "--input", type=str, nargs="?", dest="input", default=None, required=True, help="Input file or directory"
    )
    parser.add_argument("-p", "--plot", dest="plot", action="store_true", help="Plot results")

    alg_keys = list(alg_collection.keys())
    alg_keys.append("all")
    parser.add_argument(
        "-a",
        "--algorithm",
        type=str,
        nargs="?",
        dest="algorithm",
        default="all",
        choices=alg_keys,
        help="Algorithm that will be executed or all if not set",
    )
    args = parser.parse_args(parameters)
    args.action(args)


def run(args):
    print(f"Running algorithm {args.algorithm} for {args.input}")
    if args.algorithm == "all":
        for alg in alg_collection.values():
            result, bins = run_algorithm(args.input, alg)
            print_result(args.input, alg, result)
    else:
        result, bins = run_algorithm(args.input, alg_collection[args.algorithm])
        print_result(args.input, alg_collection[args.algorithm], result)


if __name__ == "__main__":
    main()
