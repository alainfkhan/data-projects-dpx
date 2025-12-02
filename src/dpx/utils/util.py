"""General purpose util functions not specific to the CLI app.
Config vars goes here
"""

import string
import random
from typing import Dict

from icecream import ic
from pandas import DataFrame, Series
from pathlib import Path
from rich.table import Table

from src.dpx.utils.paths import PROJECTS_DIR, PLAYGROUND_DIR

"""Configuration variables"""

# temporary file prefix
temp_prefix = "~"

copy_attachment = "-copy"
random_string_length = 6


def random_string(length: int = random_string_length) -> str:
    """Generate any random string."""
    characters: str = string.ascii_lowercase + string.digits

    output: str = ""
    for _ in range(length):
        output += random.choice(characters)

    return output


# def mkdir_project(project_name: str) -> Dict[str, Path]:
#     new_project_dir: Path = PROJECTS_DIR / project_name
#     (new_project_dir).mkdir()
#     return {project_name: new_project_dir}


# def mkdir_data_folders(project_dir: Path) -> Dict[str, Path]:
#     data_folders_dirs: Dict[str, Path] = {}

#     data_dir: Path = project_dir / "data"

#     for name in data_folder_names:
#         data_folder: Path = data_dir / name
#         Path(data_folder).mkdir(parents=True, exist_ok=True)
#         data_folders_dirs[name] = data_folder

#     return data_folders_dirs


# def csv_to_excel(csv_file: Path) -> None:
#     pass


def df_to_table(df: DataFrame) -> Table:
    """Pandas dataframe to rich table"""

    col_names: list[str] = list(df.columns)
    table = Table()

    for col in col_names:
        table.add_column(col)

    for row_tuple in df.itertuples(index=False):
        row_list = [str(x) for x in row_tuple]
        table.add_row(*row_list)

    return table
