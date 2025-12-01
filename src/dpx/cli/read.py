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

from src.dpx.utils.paths import PROJECTS_DIR
from src.dpx.utils.util import df_to_table, temp_prefix
from src.dpx.cli.util import list_project_names, Group


ide = "code"
ides = ["code", "vim"]

app = typer.Typer()



def list_valid_groups() -> list[str]:
    """A group is valid iff its a folder in projects/""" 
    dirs: list[str] = os.listdir(PROJECTS_DIR)

    valid_groups: list[str] = []
    for dir in dirs:
        if (PROJECTS_DIR / dir).is_dir():
            valid_groups.append(dir)
    
    return valid_groups


def verify_groups(group_candidates: list[str]) -> None:
    """Raises an error if a group name in groups is not a valid group"""
    for group_candidate in group_candidates:
        if group_candidate not in list_valid_groups():
            raise ValueError(f"'{group_candidate}' is not a valid project group.")


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
        List projects from the main group.

    dpx ls -p
        List projects from the playground group.

    dpx ls --all
        List projects from all project groups.

    dpx ls portfolio main playground
        List projects from groups: portfolio, main, and playground in that order.
    """

    verify_groups(groups)

    if playground:
        groups = ["playground"]
    
    if show_all:
        diff = set(list_valid_groups())
        diff.remove("main")
        diff.remove("playground")

        groups = ["main", "playground", *diff]

    df = pd.DataFrame()
    
    for group in groups:
        projects = list_project_names(group)
        non_temp_projects = [project for project in projects if not project.startswith(temp_prefix)]
        df_concat = pd.DataFrame(
            sorted(projects if show_temps else non_temp_projects),
            columns=[group]
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
