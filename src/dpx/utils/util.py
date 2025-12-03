"""General purpose util functions not specific to the CLI app.
Util functions that could be used in other programs.
"""

import string
import random
from typing import Dict

import nbformat as nbf
from icecream import ic
from nbformat import NotebookNode
from pandas import DataFrame, Series
from pathlib import Path
from rich.table import Table

from src.dpx.utils.paths import PROJECTS_DIR, PLAYGROUND_DIR


"""Configuration variables"""

# temporary file prefix
temp_prefix = "~"

copy_attachment = "-copy"
random_string_length = 6

type Tree = dict[str, None | Tree]


def random_string(length: int = random_string_length) -> str:
    """Generate any random string."""
    characters: str = string.ascii_lowercase + string.digits

    output: str = ""
    for _ in range(length):
        output += random.choice(characters)

    return output


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


def create_structure(base_path: Path, tree: Tree) -> None:
    """Creates file directories in a following the structure in tree

    if:
        at some base_path: "some/folder",
        tree = {
            "folder": {
                "file.txt": None
            }
        }
    then:
        create_structure(base_path, tree)
        creates a folder: "folder", and a file: "file.txt" inside "folder"
        in "some/folder"
            so "some/folder/folder/file.txt" exists

    """

    for folder_name, subtree in tree.items():
        folder_path = base_path / folder_name

        # If file
        if subtree is None:
            folder_path.parent.mkdir(parents=True, exist_ok=True)

            # TODO: fix notebook type checking
            # .ipynb
            if folder_path.name.endswith(".ipynb"):
                nb: NotebookNode = nbf.v4.new_notebook()
                nb["cells"].append(nbf.v4.new_code_cell())
                with open(folder_path, "w") as f:
                    nbf.write(nb, f)
                pass
            else:
                folder_path.touch(exist_ok=True)

        # If folder
        else:
            folder_path.mkdir(parents=True, exist_ok=True)
            create_structure(base_path=folder_path, tree=subtree)
