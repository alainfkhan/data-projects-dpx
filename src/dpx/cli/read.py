"""Read CLI commands

ls
dls
head
tail
begin
open
"""

import os
from pathlib import Path
from typing_extensions import Annotated
from collections.abc import Callable

import typer
import pandas as pd
from icecream import ic
from rich import print
from rich.console import Console

from src.dpx.cli.util import list_projects, verify_group, list_groups
from src.dpx.utils.paths import PROJECTS_DIR
from src.dpx.utils.util import df_to_table, temp_prefix


ide = "code"
ides = ["code", "vim"]

app = typer.Typer()


@app.command(help="List project names.")
def ls(
    groups: Annotated[list[str], typer.Argument(help="Choose the project groups.")] = [
        "main"
    ],
    playground: Annotated[
        bool, typer.Option("-p", "--playground", help="Choose the playground group.")
    ] = False,
    show_all: Annotated[
        bool, typer.Option("--all", help="List projects from all project groups.")
    ] = False,
    show_temps: Annotated[
        bool, typer.Option("-t", "--temps", help="List temporary projects.")
    ] = False,
) -> None:
    """List project names from a project group.

    dpx ls
        List all non-temp projects from the main group.

    dpx ls -p
        List all non-temp projects from the playground group.

    dpx ls -t
        List all projects including temps from the main group.
        Similar to ls -a

    dpx ls --all
        List all non-temp projects from all project groups.

    dpx ls portfolio main playground
        List all non-temp projects from groups: portfolio, main, and playground.
    """

    if playground:
        groups = ["playground"]

    for group in groups:
        verify_group(group)

    if show_all:
        diff = set(list_groups())
        diff.remove("main")
        diff.remove("playground")

        groups = ["main", "playground", *diff]

    df = pd.DataFrame()

    for group in groups:
        projects = list_projects(group)
        non_temp_projects = [
            project for project in projects if not project.startswith(temp_prefix)
        ]
        df_concat = pd.DataFrame(
            sorted(projects if show_temps else non_temp_projects), columns=[group]
        )

        df = pd.concat([df, df_concat], axis=1)

    df = df.fillna("")

    table = df_to_table(df)

    console = Console()
    console.print(table)


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
