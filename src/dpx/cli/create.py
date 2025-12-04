"""Create CLI commands only

TODO: finish init

init
dl
cdb
dpromote
"""

import os

import typer
from icecream import ic
from rich import print
from typing_extensions import Annotated

from src.dpx.cli.util import ProjectsManager, FileManager
from src.dpx.utils.util import (
    temp_prefix,
    copy_attachment,
    random_string,
)
from src.dpx.utils.paths import PROJECTS_DIR, PLAYGROUND_DIR

doptions: list[str] = ["ripe", "metal"]
# data folder name options
# ripe means raw, interim, processed, external
# metal means bronze, silver, gold, external

base_ddir = "r"
default_doption = "ripe"
current_main = "main"

app = typer.Typer()
pm = ProjectsManager()


# @app.command(help="Download a dataset to an existing project.")
# def dl(
#     name: Annotated[str, typer.Argument()],
#     url: Annotated[str, typer.Argument()],
#     playground: Annotated[bool, typer.Option()] = False,
# ) -> None:
#     pass


# @app.command()
# def dpromote(
#     name: Annotated[str, typer.Argument()],
#     playground: Annotated[bool, typer.Option()] = False,
#     ddir: Annotated[str, typer.Option()] = base_ddir,
#     ca: Annotated[str, typer.Option()] = copy_attachment,
# ) -> None:
#     pass


# @app.command("Create a database")
# def cdb(
#     name: Annotated[str, typer.Argument()],
#     dbn: Annotated[str, typer.Option()] = temp_prefix + random_string(),
# ) -> None:
#     pass


@app.command(help="Initialise a project workspace in an existing project group.")
def init(
    name: Annotated[
        str,
        typer.Argument(
            help="The name of the project you want to initialise.",
        ),
    ] = temp_prefix + random_string(),
    playground: Annotated[
        bool,
        typer.Option(
            "-p",
            "--playground",
            help="Initialise a project in playground.",
        ),
    ] = False,
    group: Annotated[
        str,
        typer.Option(
            "-g",
            "--g",
            help="Initialise a project in group.",
        ),
    ] = current_main,
    # doption: Annotated[str, typer.Option()] = doption,
    url: Annotated[
        str | None,
        typer.Option(
            "-u",
            "--url",
        ),
    ] = None,
    force: Annotated[
        bool,
        typer.Option(
            "-f",
            "--force",
        ),
    ] = False,
) -> None:
    """Initialises a workspace.

    dpx init smith-somedataset
        Initialise a workspace called 'smith-somedataset' in the main group.

    dpx init smith-somedataset -url <url> -g <group>
        Initialise a project called 'smith-somedataset'
        with data downloaded from <url>
        in group <group>
    """

    pm.verify_group(group)
    if not pm.can_create_project(name):
        raise ValueError(f"Project '{name}' cannot be created.")

    if playground:
        group = "playground"

    this_project_path = PROJECTS_DIR / group / name
    this_project_path.mkdir(exist_ok=True)

    # make data folders
    fm = FileManager(this_project_path)
    fm.mkdir_data_folders()

    # make other init folders
    fm.mkdir_other_files()

    # if url valid download to data/raw
    # add url to sources.txt

    print(f"Initialised new project: '{name}' in group: '{group}'.")
