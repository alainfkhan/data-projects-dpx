"""Read CLI commands

ls
dls
head
tail
begin
open
"""

import os
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing_extensions import Annotated

import pandas as pd
import typer
from icecream import ic
from pandas import DataFrame
from rich import print
from rich.console import Console
from rich.table import Table

from src.dpx.cli.utils.util import Project, ProjectManager
from src.dpx.utils.paths import PROJECTS_DIR
from src.dpx.utils.util import df_to_table, temp_prefix


ide = "code"
ides = ["code", "vim"]
current_main = "main"
app = typer.Typer()


@app.command(help="List project(s) in group(s).")
def ls(
    groups: Annotated[
        list[str],
        typer.Argument(
            help="List projects in group(s).",
        ),
    ] = [current_main],
    playground: Annotated[
        bool,
        typer.Option(
            "-p",
            "--playground",
            help="List projects in playground.",
        ),
    ] = False,
    show_all: Annotated[
        bool,
        typer.Option(
            "--all",
            help="List projects from all groups.",
        ),
    ] = True,
    temps: Annotated[
        bool,
        typer.Option(
            "-t",
            "--temps",
            help="Show temporary projects.",
        ),
    ] = False,
    show_all_temps: Annotated[
        bool,
        typer.Option(
            "--all-temps",
            help="Show temporary projects in all groups. The same as '--all --temps'",
        ),
    ] = False,
) -> None:
    """Examples:

    dpx ls
        List all non-temp projects from the main group.

    dpx ls -p
        List all non-temp projects from playground.

    dpx ls -t
        List all projects including temps from the main group.
        Similar to the UNIX command: ls -a

    dpx ls --all-temps
        List all non-temp projects from all project groups.
        The same as: dpx ls --all --temps

    dpx ls portfolio main playground
        List all non-temp projects from groups: portfolio, main, and playground, respectively.
    """

    project_manager = ProjectManager()

    for group in groups:
        project_manager.verify_group(group)

    if playground:
        groups.append("playground")

    if show_all_temps:
        show_all = True
        temps = True

    if show_all:
        groups = project_manager.groups

    df = pd.DataFrame()
    for group in groups:
        t = project_manager.list_projects_paths([group], show_non_temps=False)

        projects = project_manager.list_projects([group], show_temps=temps)

        df_concat = pd.DataFrame(
            sorted(projects),
            columns=[f"[{len(projects)}]{f' ({len(t)})' if temps else ''} {group}/"],
        )
        df = pd.concat([df, df_concat], axis=1)

    df: DataFrame = df.fillna("")

    table: Table = df_to_table(df)

    console = Console()
    console.print(table)


@app.command(help="List groups.")
def gls(
    show_hidden: Annotated[
        bool,
        typer.Option(
            "-a",
            help="Show hidden project folders.",
        ),
    ] = False,
) -> None:
    # hotfix
    exclude_files = [".git", ".gitignore", ".DS_Store", "README.md"]

    project_manager = ProjectManager()

    to_show: list[str] = []

    groups: list[str] = project_manager.groups
    to_show += groups
    if show_hidden:
        all_dirs: list[str] = os.listdir(PROJECTS_DIR)
        to_show += sorted(list(set(all_dirs).difference(set(groups)).difference(set(exclude_files))))

    print(to_show)
    return


@app.command(help="List datafiles in a project.")
def dls(
    name: Annotated[
        str,
        typer.Argument(
            help="The project name.",
        ),
    ],
    playground: Annotated[
        bool,
        typer.Option(
            "-p",
            "--p",
            help="Choose a project in playground.",
        ),
    ] = False,
    # group: Annotated[
    #     str,
    #     typer.Option(
    #         "-g",
    #         "--group",
    #         help="Choose the group of the project.",
    #     ),
    # ] = current_main,
    # ddir: Annotated[str, typer.Option()],
    # ddirs: Annotated[list[str], typer.Option()],
) -> None:
    if playground:
        group = "playground"

    project_manager = ProjectManager()

    project_manager.verify_project(name)
    group = project_manager.get_group_from_project(name)

    this_project_path = PROJECTS_DIR / group / name
    project = Project(this_project_path)

    df = project.data_ls()

    for col in df.columns:
        df.rename(columns={col: f"[{df[col].notna().sum()}] {col}/"}, inplace=True)

    df.fillna("", inplace=True)

    table: Table = df_to_table(df)
    table.title = f"{group}/{name}/data/"

    console = Console()
    console.print(table)


@app.command(help="Find the project path.")
def where(
    name: Annotated[
        str,
        typer.Argument(
            help="The name of the project.",
        ),
    ],
) -> None:
    project_manager = ProjectManager()
    project_path = project_manager.get_project_path(name)

    if project_path.exists():
        print(project_path)


# @app.command()
# def head(
#     name: Annotated[str, typer.Argument()],
#     playground: Annotated[bool, typer.Option()] = False,
#     number: Annotated[int, typer.Option()] = 10,
# ) -> None:
#     pass


# @app.command()
# def tail(
#     name: Annotated[str, typer.Argument()],
#     playground: Annotated[bool, typer.Option()] = False,
#     number: Annotated[int, typer.Option()] = 10,
# ) -> None:
#     pass


@app.command()
def begin(
    name: Annotated[str, typer.Argument()],
    playground: Annotated[
        bool,
        typer.Option(
            "-p",
            "--playground",
            help="Choose playground.",
        ),
    ] = False,
    group: Annotated[
        str,
        typer.Option(
            "-g",
            "--group",
            help="The group of the project",
        ),
    ] = current_main,
    ide: Annotated[str, typer.Option] = ide,
) -> None:
    """Begin working on the project by opening an IDE."""

    project_manager = ProjectManager()

    project_manager.verify_group(group)
    project_manager.verify_project(name)

    if playground:
        group = "playground"

    this_project_path = PROJECTS_DIR / group / name
    # project = Project(this_project_path)

    subprocess.run([ide, this_project_path])


# @app.command()
# def open(
#     name: Annotated[str, typer.Argument()],
#     playground: Annotated[bool, typer.Option()],
#     ddir: Annotated[str, typer.Argument()],
#     dname: Annotated[str, typer.Argument()],
# ) -> None:
#     pass
