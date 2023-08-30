from os import makedirs
from os.path import exists
from data_operations.data_operations import DataOperations


def generate_input_data() -> None:
    dg = DataOperations()
    packages_size = [10, 100, 1000]
    packages_max_size = [5, 10, 25]
    box_dim = [5, 10, 25]
    path = "./data/in"

    if not exists(path):
        makedirs(path)

    for size in packages_size:
        for box_width in box_dim:
            for box_height in box_dim:
                for max_width in packages_max_size:
                    for max_height in packages_max_size:
                        if max_width > box_width or max_height > box_height:
                            continue
                        df = dg.generate_input_data(box_width, box_height, max_width, max_height, size)
                        file_name = dg.generate_input_file_name(box_width, box_height, max_width, max_height, size, 0)
                        dg.save_to_file(path + "/" + file_name, df)


def generate_plotting_data() -> None:
    dg = DataOperations()
    packages_size = [10, 10, 100, 100, 50]
    packages_max_size = [5, 10, 10, 25, 10]
    box_dim = [5, 10, 10, 25, 20]
    path = "./data/plot"

    if not exists(path):
        makedirs(path)

    for size, box_width, box_height, max_width, max_height in zip(
        packages_size, box_dim, box_dim, packages_max_size, packages_max_size
    ):
        df = dg.generate_input_data(box_width, box_height, max_width, max_height, size)
        file_name = dg.generate_input_file_name(box_width, box_height, max_width, max_height, size, 0)
        dg.save_to_file(path + "/" + file_name, df)
