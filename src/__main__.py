import os
import re
import subprocess
import shutil
from pathlib import Path
from typing import Set

import kaggle
import nbformat as nbf
import pandas as pd
import typer
import openpyxl
from icecream import ic
from pandas import DataFrame, Series
from requests.exceptions import HTTPError
from rich import print
from rich.console import Console
from rich.table import Table
from urllib.parse import urlparse

from src.utils.paths import PROJECTS_DIR, PLAYGROUND_DIR, BASE_DIR
from src.utils.util import (
    random_string,
    mkdir_project,
    mkdir_data_folders,
    csv_to_excel,
    df_to_table,
)

lines = "-" * 40
unwanted_strs = ("__", ".")

app = typer.Typer()


class ProjectsManager:
    def init(self) -> None:
        pass

    pass


class KaggleProjectManager:
    protocol = "https://"
    valid_kaggle_url = "www.kaggle.com"

    def _is_kaggle_url(self, url: str) -> bool:
        parsed_url = urlparse(url=url)
        return parsed_url.netloc == self.valid_kaggle_url

    # def _get_handle_from_url(self) -> str:
    #     """https://www.kaggle.com/datasets/johnsmith/somedataset/data... -> johnsmith/somedataset"""

    #     handle: str = self.kaggle_url.removeprefix(
    #         f"https://{self.valid_kaggle_url}/datasets/"
    #     ).split("/data")[0]
    #     return handle

    def __init__(self, kaggle_url: str, project_name: str) -> None:
        if not self._is_kaggle_url(kaggle_url):
            raise ValueError("Not a valid kaggle url.")

        splits = kaggle_url.removeprefix(self.protocol).split("/")
        dataset_name_splits = splits[3].split("?")
        dataset_name = dataset_name_splits[0]

        handle: str = f"{splits[2]}/{dataset_name}"
        clean_url: str = f"{self.protocol}{splits[0]}/{splits[1]}/{handle}"

        self.project_name = project_name
        self.kaggle_url = clean_url
        self.handle = handle

    # def init_kaggle(self) -> None:
    #     project_path: Path = PROJECTS_DIR / self.project_name

    #     # Make project folder
    #     mkdir_project(self.project_name)

    #     # Make data folders in the newly created project folder
    #     data_folders_paths = mkdir_data_folders(project_path)
    #     raw_path: Path = data_folders_paths["raw"]
    #     external_path: Path = data_folders_paths["external"]

    #     # Download dataset from kaggle
    #     kaggle.api.authenticate()

    #     try:
    #         kaggle.api.dataset_download_files(
    #             dataset=self.handle, path=raw_path, unzip=True
    #         )
    #     except HTTPError as e:
    #         print(e)
    #         print("Kaggle dataset not found. Please verify the kaggle URL is correct.")
    #     else:
    #         kaggle.api.dataset_metadata(dataset=self.handle, path=external_path)

    #     print("The dataset has been succefully downloaded")
    #     return

    def download_to(self, project: Path) -> None:
        raw_path: Path = project / "data" / "raw"
        external_path: Path = project / "data" / "external"

        kaggle.api.authenticate()

        try:
            kaggle.api.dataset_download_files(
                dataset=self.handle, path=raw_path, unzip=True
            )
        except HTTPError as e:
            print(e)
            print(
                "Kaggle dataset not found. Verify the kaggle URL is correct."
            )
        else:
            kaggle.api.dataset_metadata(
                dataset=self.handle, path=external_path
            )

        # print("The dataset has been successfully downloaded.")

        pass

    def copy_all_files(self) -> None:
        pass


# ======================================================================
# HELPER FUNCTIONS
# ======================================================================


def _find_project_dirs(
    home: Path = PROJECTS_DIR,
    temps_only: bool = False,
    non_temps_only: bool = False,
) -> set[Path]:
    dir_names: list[str] = os.listdir(home)

    ignore_files: list[str] = ["README.md"]

    projects: set[Path] = set()
    temps: set[Path] = set()

    for dir_name in dir_names:
        if dir_name.startswith(unwanted_strs):
            continue
        elif dir_name in ignore_files:
            continue

        if dir_name.startswith("~"):
            temps.add(home / dir_name)

        projects.add(home / dir_name)

    if temps_only and non_temps_only:
        return projects

    if temps_only:
        return temps

    if non_temps_only:
        return projects - temps

    return projects


def _get_project_dir(name: str, playground: bool = False) -> Path:
    home_dir = PLAYGROUND_DIR if playground else PROJECTS_DIR
    return home_dir / name


def validate_project(project: Path, playground: bool = False) -> None:
    home = project.parent
    if project not in _find_project_dirs(home=home):
        raise FileNotFoundError(
            f"Project: '{project.name}' not found{' in playground' if playground else ''}."
        )


# TODO: complete
def _find_dirs_same_names(project: Path) -> list[Path]:
    """Finds the directories of the files with the same name as the input.
    Ignore data files
    """

    output: list[Path] = []

    pattern = f"*{project.name}*"
    for f in project.rglob(pattern):
        # ignore all datafiles
        if f.parent.parent.name == "data":
            continue
        else:
            output.append(f)

    output.append(project)

    return output


@app.command(help="Initialise a project.")
def init(
    name: str = typer.Argument(
        "~" + random_string(), help="Create a name for the project."
    ),
    test=typer.Argument(),
    playground: bool = typer.Option(
        False,
        "-p",
        "--playground",
        help="Initialise the project in the playground directory.",
    ),
    force: bool = typer.Option(
        False,
        "-f",
        "--force-overwrite",
        help="Forcefully overwrite existing initialisation files.",
    ),
    kaggle_url: str | None = typer.Option(
        None,
        "-ku",
        "--kaggle-url",
        help="Initialise a project with a kaggle dataset.",
    ),
) -> None:
    new_project_dir = _get_project_dir(name, playground)
    home = new_project_dir.parent
    p_option = f"{' in playground' if playground else ''}"

    # Create project directory
    try:
        new_project_dir.mkdir()
        print(f"Initialised new project: '{new_project_dir.name}'{p_option}.")
    except FileExistsError:
        if force:
            print(
                f"Overwriting initialisation files for project: '{new_project_dir.name}'{p_option}."
            )
        else:
            print(f"Project '{name}' in {home} already exists.")

    # Create data folders
    mkdir_data_folders(new_project_dir)

    # Create docs/ and reports/ folder
    (new_project_dir / "docs" / "assets").mkdir(parents=True, exist_ok=True)
    (new_project_dir / "reports").mkdir(parents=True, exist_ok=True)

    # Create default initialisation files
    project_files = os.listdir(new_project_dir)
    docs_files = os.listdir(new_project_dir / "docs")

    # Python notebook
    nb_name = f"{name}.ipynb"
    if nb_name not in project_files or force:
        # Create new notebook
        nb = nbf.v4.new_notebook()
        nb["cells"].append(nbf.v4.new_code_cell())
        with open(f"{new_project_dir}/{name}.ipynb", "w") as f:
            nbf.write(nb, f)

        # print(f"New file: '{nb_name}'")

    # README.md
    readme = "README.md"
    if readme not in project_files or force:
        with open(f"{new_project_dir}/{readme}", "w"):
            pass

        # print(f"New file: '{readme}'")

    # Sources
    sources = "sources.txt"
    if sources not in docs_files:
        with open(f"{new_project_dir}/docs/{sources}", "w"):
            pass

        # print(f"New file: '{sources}'")

    if kaggle_url:
        kaggle_pm = KaggleProjectManager(
            kaggle_url=kaggle_url, project_name=name
        )
        kaggle_pm.download_to(new_project_dir)

        # Append url to history.txt
        # TODO: append only if unique
        with open(f"{BASE_DIR}/docs/history.txt", "a") as f:
            f.write(f"\n{name}: {kaggle_pm.kaggle_url}")

        # Append url to sources.txt
        with open(f"{new_project_dir}/docs/{sources}", "a") as f:
            f.write(f"url: {kaggle_pm.kaggle_url}")


@app.command()
def dl(
    name: str = typer.Argument(help="Download the dataset in this project."),
    playground: bool = typer.Option(
        False, "-p", "--playground", help="The project lives here."
    ),
    kaggle_url: str | None = typer.Option(
        "", "-ku", "--kaggle-url", help="Download dataset from kaggle url."
    ),
) -> None:
    home: Path = PLAYGROUND_DIR if playground else PROJECTS_DIR
    this_project = _get_project_dir(name=name, playground=playground)

    is_input_url = bool(kaggle_url)

    if not is_input_url:
        raise ValueError("User must input a url.")

    validate_project(project=this_project, playground=playground)

    if kaggle_url:
        kaggle_pm = KaggleProjectManager(kaggle_url, name)
        kaggle_pm.download_to(home / name)


@app.command()
def create_db() -> None:
    pass


@app.command(help="List projects.")
def ls(
    playground: bool = typer.Option(
        False,
        "-p",
        "--playgound",
        help="List the projects in the playground.",
    ),
    temps: bool = typer.Option(
        False, "-t", "--temps", help="List temporary projects."
    ),
    non_temps: bool = typer.Option(
        False, "-nt", "--non-temps", help="List non-temporary projects."
    ),
    show_all: bool = typer.Option(False, "--all", help="List all projects."),
    show_all_temps: bool = typer.Option(
        False, "--all-temps", help="List all temporary files."
    ),
) -> None:
    def count_message(count: int) -> str:
        message = f"[{count}] {'temporary ' if temps else ''}projects found{' in playground' if playground else ''}."
        return message

    if show_all_temps:
        show_all = True
        temps = True

    projects: set[Path] = _find_project_dirs(
        PROJECTS_DIR, temps_only=temps, non_temps_only=non_temps
    )
    p_projects: set[Path] = _find_project_dirs(
        PLAYGROUND_DIR, temps_only=temps, non_temps_only=non_temps
    )

    total_projects: list[Path] = sorted(projects) + sorted(p_projects)
    # Always in the order: projects, playground projects.
    # Playground projects are always secondary.
    # 0 for projects, 1 for playground projects.

    df_projects = pd.DataFrame(
        sorted([project.name for project in projects]), columns=["Projects"]
    )
    df_playground_projects = pd.DataFrame(
        sorted([project.name for project in p_projects]),
        columns=["Playground"],
    )

    df = pd.concat([df_projects, df_playground_projects], axis=1)
    df = df.fillna("")

    if show_all:
        count = len(total_projects)
    else:
        if playground:
            df = df_playground_projects
        else:
            df = df_projects
        count = len(df)

    # df either a DataFrame or Series

    print(count_message(count))

    if count > 0:
        table = df_to_table(df)
        console = Console()
        console.print(table)

    return


@app.command()
def show() -> None:
    pass


# TODO: rename history.txt
@app.command()
def rename(
    old_to_new: list[str] = typer.Argument(
        help="The name of the file you want to rename."
    ),
    playground: bool = typer.Option(
        False, "-p", "--playground", help="Choose the file playground."
    ),
) -> None:
    if len(old_to_new) != 2:
        raise ValueError("Only list two names: name, new_name")

    old_name: str = old_to_new[0]
    new_name: str = old_to_new[1]

    home: Path = PLAYGROUND_DIR if playground else PROJECTS_DIR
    this_project: Path = home / old_name

    validate_project(project=this_project, playground=playground)

    to_rename: list[Path] = _find_dirs_same_names(this_project)

    for f in to_rename:
        old_path: Path = f.parent / f.name
        new_path: Path = f.parent / f.name.replace(old_name, new_name)

        try:
            os.rename(old_path, new_path)
        except Exception as e:
            print(e)


@app.command(help="Move a project from playground/ to projects/")
def promote() -> None:
    pass


@app.command(help="Move a project from projects/ to playground/")
def demote() -> None:
    pass


@app.command(
    help="Copies data files from raw to interim turning any .csv to .xlsx."
)
def cp(
    name: str = typer.Argument(
        help="The name of the project you want to copy data within."
    ),
    playground: bool = typer.Option(
        False,
        "-p",
        "--playground",
        help="Copy data within a project inside the playground directory.",
    ),
) -> None:
    """Any .csv files are turned into"""
    this_project: Path = _get_project_dir(name=name, playground=playground)

    raw_path: Path = this_project / "data" / "raw"
    interim_path: Path = this_project / "data" / "interim"

    copy_attachment = "-copy"

    csv_exts = [".csv"]
    xls_exts = [".xls", ".xlsx", ".xlsm"]
    # .xls .xlsx .xlsm .xlsb .xltx .xltm .xlm
    other_exts = [".tsv", ".txt"]

    for raw_file in raw_path.iterdir():
        old_name: str = raw_file.name
        old_stem: str = old_name.split(".")[0]
        old_ext: str = old_name.removeprefix(old_stem)
        # old_name = old_stem + old_ext

        new_stem: str = old_stem + copy_attachment

        # if .csv
        if old_ext in csv_exts:
            new_ext: str = ".xlsx"
            interim_file = interim_path / (new_stem + new_ext)

            data: DataFrame = pd.read_csv(raw_file)
            data.to_excel(interim_file, index=False, engine="openpyxl")

        # if any .xlsx
        if old_ext in xls_exts:
            interim_file = interim_path / old_name
            with open(interim_file, "w"):
                pass

        # if any other


@app.command(help="Delete a project.")
def rm(
    project_names: list[str] | None = typer.Argument(
        None, help="The names of the projects you want to remove."
    ),
    playground: bool = typer.Option(
        False,
        "-p",
        "--playground",
        help="Delete projects from the playground directory.",
    ),
    temps: bool = typer.Option(
        False, "-t", "--temps", help="Delete temporary projects."
    ),
    all_temps: bool = typer.Option(
        False,
        "--all-temps",
        help="Delete all temporary projects.",
    ),
) -> None:
    if project_names is None:
        project_names = []

    if all_temps:
        temps = True

    home: Path = PLAYGROUND_DIR if playground else PROJECTS_DIR

    to_delete: set[Path] = set([home / name for name in project_names])

    projects = _find_project_dirs(PROJECTS_DIR, temps_only=temps)
    p_projects = _find_project_dirs(PLAYGROUND_DIR, temps_only=temps)

    if playground:
        varset = p_projects
    else:
        varset = projects

    if all_temps:
        to_delete = to_delete.union(projects).union(p_projects)

    if temps:
        to_delete = to_delete.union(varset)

    if len(to_delete) == 0:
        raise ValueError("Requires files to delete.")

    for f in to_delete:
        try:
            shutil.rmtree(f)
            # print(f"Removed: {f.parent.name}/{f.name}.")
        except FileNotFoundError:
            print(
                f"Project: '{f.name}' does not exist inside {f.parent.name}/."
            )
            pass


@app.command(help="Begin working on the main file to start analysis.")
def begin(
    name: str = typer.Argument(
        help="The name of the project you want to start."
    ),
    playground: bool = typer.Option(
        False, "-p", "--playground", help="Choose a playground project."
    ),
) -> None:
    this_project: Path = _get_project_dir(name=name, playground=playground)

    validate_project(this_project, playground)

    try:
        subprocess.run(["code", this_project], check=True)
    except FileNotFoundError:
        print("File not found")
    except subprocess.CalledProcessError as e:
        print(f"Error launching VS code: {e}")
    except Exception as e:
        print(f"An unexpected error occured: {e}")


def main() -> None:
    app()
    # # Developer entries:
    # init_kaggle_project: bool = False
    # kaggle_url: str = (
    #     "https://www.kaggle.com/datasets/sticktogethertm/business-analysis-junior"
    # )
    # project_name: str = "panteleev-baj"

    # print("running")
    # copy_csv_files: bool = True

    # if init_kaggle_project:
    #     kaggle_project_manager = KaggleProjectManager(kaggle_url, project_name)
    #     print(f"Initialising kaggle project {kaggle_project_manager.handle}")
    #     kaggle_project_manager.init_kaggle()
    #     print("Initialisation complete.")
    #     return


if __name__ == "__main__":
    main()
