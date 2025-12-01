"""Delete CLI commands.

TODO: rm moves a project to trash, until deletion some days later

rm
"""

import shutil
from pathlib import Path
from typing_extensions import Annotated

import typer
from icecream import ic
from rich import print

from src.dpx.cli.util import ProjectsManager
from src.dpx.utils.paths import PROJECTS_DIR

app = typer.Typer()
pm = ProjectsManager()


@app.command()
def rm(
    names: Annotated[list[str] | None, typer.Argument()] = None,
    group: Annotated[str, typer.Option("-g", "--group")] = "main",
    playground: Annotated[bool, typer.Option("-p", "--playground")] = False,
    search_all: Annotated[bool, typer.Option("--all")] = False,
    temps: Annotated[bool, typer.Option("-t", "--temps")] = False,
    rm_all_temps: Annotated[bool, typer.Option("--all-temps")] = False,
) -> None:
    """Delete projects.

    dpx rm test
        Removes project 'test' in group main.

    dpx rm test dataset --all-groups
        Searches all groups and removes projects 'test' and 'dataset'

    dpx rm -t -p
        Removes all temp projects in playground.

    dpx rm --all-temps
    dpx rm -t --all-groups
        Searches all groups and removes all temp projects.
    """

    def delete(filepaths: list[Path]) -> None:
        for f in filepaths:
            try:
                shutil.rmtree(f)
            except FileNotFoundError:
                print(f"'{f.name}' not a project in '{f.parent.name}'")
        pass

    if rm_all_temps:
        search_all = True
        temps = True

    if names is None and not temps:
        raise ValueError("Requires project name or temps option.")

    if playground:
        group = "playground"

    group_path = PROJECTS_DIR / group
    to_remove: list[Path] = []

    if temps:
        temp_projects = pm.list_project_paths(
            pm.groups if search_all else [group], show_non_temps=False
        )
        to_remove = to_remove + temp_projects

    if names is not None:
        for name in names:
            pm.verify_project(name)
            to_remove.append(group_path / name)

    delete(to_remove)

    # search_scope = pm.all_projects if search_all_groups else pm.list_projects_OLD(group)
    # for name in names:
    #     if name not in search_scope:
    #         print(
    #             f"Could not find project: '{name}' in {'any group' if search_all_groups else f"group: '{group}'"}."
    #         )
    #     to_remove.append(PROJECTS_DIR / group / name)
    #     ic(f"removing {name}")

    # if all_temps:
    #     temps = True

    # if temps:
    #     ic(pm.all_project_paths)
    #     ic(pm.all_temps_paths)
