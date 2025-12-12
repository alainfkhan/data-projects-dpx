"""Delete CLI commands.

TODO: rm moves a project to trash, until deletion some days later

rm
"""

import os
import shutil
import threading
from pathlib import Path
from typing_extensions import Annotated

import typer
from icecream import ic
from rich import print

from src.dpx.cli.utils.util import ProjectManager, Project
from src.dpx.utils.paths import PROJECTS_DIR

app = typer.Typer()
current_main = "main"
wait_to_unlock: int = 10


@app.command(help="Delete project(s).")
def project(
    names: Annotated[
        list[str] | None,
        typer.Argument(
            help="The name of the project(s) you want to delete.",
        ),
    ] = None,
    group: Annotated[
        str,
        typer.Option(
            "-g",
            "--group",
            help="Search in a group.",
        ),
    ] = current_main,
    playground: Annotated[
        bool,
        typer.Option(
            "-p",
            "--playground",
            help="Search in playground.",
        ),
    ] = False,
    search_all: Annotated[
        bool,
        typer.Option(
            "--all",
            help="Search in all groups.",
        ),
    ] = False,
    temps: Annotated[
        bool,
        typer.Option(
            "-t",
            "--temps",
            help="Remove all temporary projects in a selection of groups.",
        ),
    ] = False,
    rm_all_temps: Annotated[
        bool,
        typer.Option(
            "--all-temps",
            help="Remove all temporary projects in all groups. The same as '--all --temps'",
        ),
    ] = False,
) -> None:
    """Examples:

    dpx rm test1
        Delete 'test1' in the main group.

    dpx rm test1 test2
        Delete 'test1' and 'test2' in the main group.

    dpx rm playgroundp -p
        Dalete 'playgroundp' in playground.

    dpx rm mainp playgroundp --all
        Delete 'mainp' and 'playgroundp' searching all groups.

    dpx rm -t -p
        Delete all temporary projects in playground.

    dpx rm --all -t
        Delete all temporary projects searching in all groups.
    """

    project_manager = ProjectManager()

    def delete(filepaths: list[Path]) -> None:
        """Want to change to move to .trash/"""
        if len(filepaths) == 0:
            print("No files deleted.")
            return

        unlocked_projects: list[str] = []
        for f in filepaths:
            if not f.exists():
                # file not found error
                print(f"'{f.name}' not a project in '{f.parent.name}'")
                continue

            project = Project(f)
            if project.is_locked():
                # print(f"'{project.name}' was not deleted. Must be unlocked first.")
                unlocked_projects.append(project.name)
            else:
                shutil.rmtree(f)
                print(f"'{f.name}' deleted from '{f.parent.name}'")
                continue

        if unlocked_projects:
            plural = len(unlocked_projects) > 1
            for p in unlocked_projects:
                print(f"'{p}'", end=", " if plural else " ")
            print(f"must be unlocked before {'they are' if plural else 'it is'} deleted.")

    if rm_all_temps:
        search_all = True
        temps = True

    if names is None and not temps:
        raise ValueError("Requires at least one project or temps option.")

    if playground:
        group = "playground"

    to_remove: list[Path] = []

    if temps:
        temp_projects = project_manager.list_projects_paths(
            project_manager.groups if search_all else [group],
            show_non_temps=False,
        )
        to_remove = to_remove + temp_projects

    if names is not None:
        for name in names:
            project_manager.verify_project(name)
            group = project_manager.get_group_from_project(name) if search_all else group

            to_remove.append(PROJECTS_DIR / group / name)

    delete(to_remove)

    # search_scope = pm.all_projects if search_all_groups else pm.list_projects_OLD(group)
    # for name in names:
    #     if name not in search_scope:
    #         print(
    #             f"Could not find project: '{name}' in {'any group' if search_all_groups else f"group: '{group}'"}."
    #         )
    #     to_remove.append(PROJECTS_DIR / group / name)


@app.command()
def group(group: Annotated[str, typer.Argument()]) -> None:
    project_manager = ProjectManager()

    projects_in_group = project_manager.list_projects([group])
    if projects_in_group:
        print(f"Cannot delete group: '{group}'. Empty first.")
    else:
        os.rmdir(PROJECTS_DIR / group)
        print(f"Deleted group: '{group}'.")
