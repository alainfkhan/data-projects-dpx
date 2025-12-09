"""Update CLI commands.

rename
drename
uds
promote
demote
mv
"""

import os
from typing_extensions import Annotated
from pathlib import Path

import typer
from icecream import ic
from rich import print

from src.dpx.cli.utils.util import Project, ProjectManager
from src.dpx.utils.paths import PROJECTS_DIR
from src.dpx.utils.util import find_dirs_with_name

app = typer.Typer()
current_main = "main"


@app.command(help="Unlock project(s).")
def unlock(
    names: Annotated[
        list[str] | None,
        typer.Argument(help="The name of the project you want to unlock."),
    ] = None,
    playground: Annotated[
        bool,
        typer.Option("-p", "--playground", help="Unlock a project in playground."),
    ] = False,
    group: Annotated[
        str,
        typer.Option("-g", "--group", help="The group the project lives."),
    ] = current_main,
) -> None:
    """Want to add resistance deleting a project."""

    if names is None:
        raise ValueError("Requires at least one project.")

    if playground:
        group = "playground"

    for name in names:
        this_project_path = PROJECTS_DIR / group / name
        if this_project_path.exists():
            project = Project(this_project_path)
        else:
            print(f"'{name}' does not exist in '{group}.'")
            continue

        if not project.is_locked():
            print(f"'{project.name}' in '{project.group}' is already unlocked.")
        else:
            project.unlock()
            print(f"Unlocked '{project.name}' in '{project.group}'.")


@app.command()
def lock(
    names: Annotated[
        list[str] | None,
        typer.Argument(help="The name of the project you want to lock."),
    ] = None,
    playground: Annotated[
        bool,
        typer.Option("-p", "--playground", help="Lock a project in playground."),
    ] = False,
    group: Annotated[
        str,
        typer.Option("-g", "--group", help="The group the project lives."),
    ] = current_main,
    lock_all: Annotated[
        bool,
        typer.Option(
            "--all",
            help="Lock all projects in all groups.",
        ),
    ] = False,
) -> None:
    if lock_all:
        project_manager = ProjectManager()
        all_projects_paths = project_manager.list_projects_paths()

        for p in all_projects_paths:
            project = Project(p)
            project.lock()
        return

    if names is None:
        raise ValueError("Requires at least one project.")

    if playground:
        group = "playground"

    for name in names:
        this_project_path = PROJECTS_DIR / group / name
        if this_project_path.exists():
            project = Project(this_project_path)
        else:
            print(f"'{name}' does not exist in '{group}.'")
            continue

        if project.is_locked():
            print(f"'{project.name}' in '{project.group}' is already locked.")
        else:
            project.lock()
            print(f"Locked '{project.name}' in '{project.group}'.")


@app.command()
def rename(
    name_to_new: Annotated[
        list[str],
        typer.Argument(
            help="From name to new name",
        ),
    ],
    playground: Annotated[
        bool,
        typer.Option(
            "-p",
            "--playground",
            help="Rename a project in playground.",
        ),
    ] = False,
    group: Annotated[
        str,
        typer.Option(
            "-g",
            "--group",
            help="Rename a project in group.",
        ),
    ] = current_main,
) -> None:
    """Rename an existing project including all sub files with the same name."""

    if len(name_to_new) != 2:
        raise ValueError("Must have exactly two entries.")

    old_name = name_to_new[0]
    new_name = name_to_new[1]

    project_manager = ProjectManager()
    project_manager.verify_group(group)
    project_manager.verify_project(old_name)
    project_manager.can_create_project(new_name)

    if playground:
        group = "playground"

    this_old_project_path = PROJECTS_DIR / group / old_name

    if not this_old_project_path.exists():
        print(f"'{old_name}' is not in '{group}'")
        return

    dirs: list[Path] = find_dirs_with_name(old_name, this_old_project_path)
    dirs.append(this_old_project_path)

    for dir in dirs:
        old_dir_name = dir
        new_dir_name = dir.parent / dir.name.replace(old_name, new_name)

        try:
            os.rename(old_dir_name, new_dir_name)
        except Exception as e:
            print(e)


# @app.command()
# def drename(
#     name: Annotated[str, typer.Argument("-n")],
#     dname_to_new: Annotated[list[str], typer.Argument()],
#     ddir: Annotated[str, typer.Argument()],
#     playground: Annotated[bool, typer.Option()] = False,
# ) -> None:
#     pass


# @app.command()
# def uds(do_all: Annotated[bool, typer.Option()] = False) -> None:
#     pass


# @app.command()
# def promote(name: Annotated[str, typer.Argument()]) -> None:
#     pass


# @app.command()
# def demote(name: Annotated[str, typer.Argument()]) -> None:
#     pass


# @app.command()
# def mv(name: Annotated[str, typer.Argument()]) -> None:
#     pass
