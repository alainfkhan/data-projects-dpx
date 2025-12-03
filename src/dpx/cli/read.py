"""Read CLI commands

ls
dls
head
tail
begin
open
"""

import os
from collections.abc import Callable
from pathlib import Path
from typing_extensions import Annotated

import typer
import pandas as pd
from icecream import ic
from rich import print
from rich.console import Console
from rich.table import Table

from src.dpx.cli.util import ProjectsManager
from src.dpx.utils.paths import PROJECTS_DIR
from src.dpx.utils.util import df_to_table, temp_prefix


ide = "code"
ides = ["code", "vim"]
current_main = "main"
app = typer.Typer()
pm = ProjectsManager()


@app.command(help="List project(s).")
def ls(
    groups: Annotated[list[str], typer.Option("-g", "--group", help="List projects in group(s).")] = [current_main],
    playground: Annotated[
        bool,
        typer.Option("-p", "--playground", help="List projects in playground."),
    ] = False,
    show_all: Annotated[
        bool,
        typer.Option("--all", help="List projects from all groups."),
    ] = False,
    temps: Annotated[bool, typer.Option("-t", "--temps", help="Show temporary projects.")] = False,
    show_all_temps: Annotated[
        bool, typer.Option("--all-temps", help="Show temporary projects in all groups. The same as '--all --temps'")
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

    for group in groups:
        pm.verify_group(group)

    if playground:
        groups = ["playground"]

    if show_all_temps:
        show_all = True
        temps = True

    if show_all:
        diff = pm.groups
        diff.remove("main")
        diff.remove("playground")

        groups = ["main", "playground", *sorted(diff)]

    df = pd.DataFrame()
    for group in groups:
        t = pm.list_projects_paths([group], show_non_temps=False)

        projects = pm.list_projects([group], show_temps=temps)

        df_concat = pd.DataFrame(
            sorted(projects),
            columns=[f"[{len(projects)}]{f' ({len(t)})' if temps else ''} {group}/"],
        )
        df = pd.concat([df, df_concat], axis=1)

    df = df.fillna("")

    table: Table = df_to_table(df)

    console = Console()
    console.print(table)


@app.command(help="List groups.")
def gls(
    toggle_unreachable: Annotated[bool, typer.Option("-f", help="Show unreachable project folders.")] = False,
) -> None:
    exclude_files = {".git", ".DS_Store", ".gitignore", "README.md"}

    groups = pm.groups
    if toggle_unreachable:
        all_dirs = set(os.listdir(PROJECTS_DIR))
        to_show = all_dirs.difference(set(groups)).difference(exclude_files)

        print(to_show)
    else:
        print(groups)

    return


# @app.command()
# def dls(
#     name: Annotated[str, typer.Argument()],
#     playground: Annotated[bool, typer.Option()],
#     ddir: Annotated[str, typer.Option()],
#     ddirs: Annotated[list[str], typer.Option()],
# ) -> None:
#     pass


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


# @app.command()
# def begin(
#     name: Annotated[str, typer.Argument()],
#     playground: Annotated[bool, typer.Option()],
#     ide: Annotated[str, typer.Option] = ide,
# ) -> None:
#     pass


# @app.command()
# def open(
#     name: Annotated[str, typer.Argument()],
#     playground: Annotated[bool, typer.Option()],
#     ddir: Annotated[str, typer.Argument()],
#     dname: Annotated[str, typer.Argument()],
# ) -> None:
#     pass
