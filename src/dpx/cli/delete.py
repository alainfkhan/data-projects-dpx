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
current_main = "main"


@app.command()
def rm(
    names: Annotated[list[str] | None, typer.Argument()] = None,
    group: Annotated[str, typer.Option("-g", "--group")] = current_main,
    playground: Annotated[bool, typer.Option("-p", "--playground")] = False,
    search_all: Annotated[bool, typer.Option("--all")] = False,
    temps: Annotated[bool, typer.Option("-t", "--temps")] = False,
    rm_all_temps: Annotated[bool, typer.Option("--all-temps")] = False,
) -> None:
    """Delete projects.

    dpx rm test
        Removes project 'test' in group main.

    dpx rm test dataset --all
        Searches all groups and removes projects 'test' and 'dataset'

    dpx rm -t -p
        Removes all temp projects in playground.

    dpx rm --all-temps
    dpx rm -t --all
        Searches all groups and removes all temp projects.
    """

    def delete(filepaths: list[Path]) -> None:
        for f in filepaths:
            try:
                # shutil.rmtree(f)
                print(f"'{f.name}' deleted from '{f.parent.name}'")
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

    to_remove: list[Path] = []

    if temps:
        temp_projects = pm.list_projects_paths(
            pm.groups if search_all else [group], show_non_temps=False
        )
        to_remove = to_remove + temp_projects

    if names is not None:
        for name in names:
            pm.verify_project(name)
            to_remove.append(PROJECTS_DIR / pm.get_group_from_project(name) / name)

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


@app.command()
def dev(input: Annotated[str, typer.Option()] = "") -> None:

    groups = pm.groups
    p_path = pm.list_projects_paths(groups)

    # p = pm.list_projects(groups)

    ic(p_path)
