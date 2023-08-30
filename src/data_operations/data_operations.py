from os import listdir
from os.path import isfile, join
import pandas
import random
from typing import Dict


class DataOperations:
    def __init__(self):
        random.seed()
        pass

    @staticmethod
    def generate_input_data(
        box_width: int, box_height: int, max_width: int, max_height: int, size: int
    ) -> pandas.DataFrame:
        val_dict = {"width": [box_width], "height": [box_height]}

        for _ in range(size):
            val_dict["width"].append(random.randint(1, max_width))
            val_dict["height"].append(random.randint(1, max_height))

        return pandas.DataFrame(val_dict)

    @staticmethod
    def generate_input_file_name(
        box_width: int, box_height: int, max_width: int, max_height: int, size: int, num: int
    ) -> str:
        return f"s_{size}_b_{box_width}_{box_height}_p_{max_width}_{max_height}_n_{num}.in"

    @staticmethod
    def parse_input_file_name(file_name: str) -> Dict[str, int] | None:
        data = file_name.split("_")
        if len(data) == 10:
            return {
                "size": int(data[1]),
                "box_width": int(data[3]),
                "box_height": int(data[4]),
                "max_width": int(data[6]),
                "max_height": int(data[7]),
                "num": int(data[9].split(".")[0]),
            }
        return None

    @staticmethod
    def save_to_file(path: str, df: pandas.DataFrame) -> None:
        df.to_csv(path, header=True, index=False)

    @staticmethod
    def load_from_file(path) -> pandas.DataFrame:
        return pandas.read_csv(filepath_or_buffer=path)

    @staticmethod
    def get_all_input_files(directory: str):
        return [file for file in listdir(directory) if isfile(join(directory, file))]
