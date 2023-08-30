from collections import defaultdict
from dataclasses import dataclass
from tabulate import tabulate
from typing import List


@dataclass
class PackingResult:
    bins_num: int
    packages_num: int
    package_max_width: int
    package_max_height: int
    bin_max_width: int
    bin_max_height: int


class PackingStats:
    def __init__(self):
        self.results = defaultdict(list[PackingResult])

    def add_result(self, algorithm_name: str, res: PackingResult):
        self.results[algorithm_name].append(res)

    def print_results_for_algorithm(self, algorithm_name: str):
        names = ["Packages num", "Package max size", "Bin size", "Bins num"]
        report: List[List] = []

        for el in self.results[algorithm_name]:
            report.append(
                [
                    el.packages_num,
                    f"{el.package_max_width}x{el.package_max_height}",
                    f"{el.bin_max_width}x{el.bin_max_height}",
                    el.bins_num,
                ]
            )

        print("Results for algorithm " + algorithm_name)
        print(tabulate(report, names, numalign="center", tablefmt="pretty"))

    def print_results_for_algorithm_short(self, algorithm_name: str, group_column: int):
        names = ["Packages num", "Package max size", "Bin size", "Bins num"]
        report: List[List] = []

        for el in self.results[algorithm_name]:
            report.append(
                [
                    el.packages_num,
                    f"{el.package_max_width}x{el.package_max_height}",
                    f"{el.bin_max_width}x{el.bin_max_height}",
                    el.bins_num,
                ]
            )

        print("Results for algorithm " + algorithm_name)
        print(tabulate(report, names, numalign="center", tablefmt="pretty"))
