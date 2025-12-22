"""Update CLI commands.

rename
drename
uds
promote
demote
mv
"""

import os
import shutil
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
    # playground: Annotated[
    #     bool,
    #     typer.Option("-p", "--playground", help="Unlock a project in playground."),
    # ] = False,
    # group: Annotated[
    #     str,
    #     typer.Option("-g", "--group", help="The group the project lives."),
    # ] = current_main,
) -> None:
    """Want to add resistance deleting a project."""

    if names is None:
        raise ValueError("Requires at least one project.")

    # if playground:
    #     group = "playground"
    project_manager = ProjectManager()

    for name in names:
        group = project_manager.get_group_from_project(name)
        this_project_path = project_manager.get_project_path(name)
        # this_project_path = PROJECTS_DIR / group / name
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
    # playground: Annotated[
    #     bool,
    #     typer.Option("-p", "--playground", help="Lock a project in playground."),
    # ] = False,
    # group: Annotated[
    #     str,
    #     typer.Option("-g", "--group", help="The group the project lives."),
    # ] = current_main,
    lock_all: Annotated[
        bool,
        typer.Option(
            "-a",
            "--all",
            help="Lock all projects in all groups.",
        ),
    ] = False,
) -> None:
    project_manager = ProjectManager()

    if lock_all:
        groups = project_manager.groups
        all_projects_paths = project_manager.list_projects_paths(groups)

        for p in all_projects_paths:
            project = Project(p)
            project.lock()
        return

    if names is None:
        raise ValueError("Requires at least one project.")

    # if playground:
    #     group = "playground"

    for name in names:
        group = project_manager.get_group_from_project(name)
        this_project_path = project_manager.get_project_path(name)
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
def islocked(
    name: Annotated[
        str,
        typer.Argument(
            help="The name of the project.",
        ),
    ],
) -> None:
    project_manager = ProjectManager()
    project_manager.verify_project(name)

    this_project_path = project_manager.get_project_path(name)
    project = Project(this_project_path)
    print(project.is_locked())


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


@app.command()
def add_sources(
    things: Annotated[
        list[str],
        typer.Argument(
            help="The source you want to append to the projects's sources.txt",
        ),
    ],
    name: Annotated[
        str,
        typer.Option(
            "-n",
            "--name",
            help="The name of the project.",
        ),
    ],
) -> None:
    """Appends sources to the sources.txt

    dpx add-sources url1 url2 -n smith-somedataset
        Appends url1, url2 to the sources folder in project: smith-somedataset


    """
    project_manager = ProjectManager()
    project_manager.verify_project(name)

    project = Project(project_manager.get_project_path(name))

    for t in things:
        project.append_source(t)


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


@app.command(help="Move a file from one group to another group.")
def mv(
    names: Annotated[
        list[str],
        typer.Argument(
            help="The name of the project(s).",
        ),
    ],
    to_group: Annotated[
        str,
        typer.Option(
            "-to",
            help="Move the file to this group.",
        ),
    ],
    # playground: Annotated[
    #     bool,
    #     typer.Option(
    #         "-p",
    #         "--playground",
    #         help="Choose the playground group.",
    #     ),
    # ] = False,
    # group: Annotated[
    #     str,
    #     typer.Option(
    #         "-g",
    #         "--group",
    #         help="The name of the group.",
    #     ),
    # ] = current_main,
) -> None:
    project_manager = ProjectManager()
    project_manager.verify_group(to_group)

    moved_projects: list[str] = []
    same_dst_projects: list[str] = []
    locked_projects: list[str] = []
    for name in names:
        project = Project(project_manager.get_project_path(name))
        if project.is_locked():
            locked_projects.append(name)
            continue

        project_manager.verify_project(name)

        group = project_manager.get_group_from_project(name)
        if group == to_group:
            same_dst_projects.append(name)
            continue

        project.lock()

        src = PROJECTS_DIR / group / name
        dst = PROJECTS_DIR / to_group / name
        shutil.move(src, dst)

        moved_projects.append(name)

    if moved_projects:
        print("Moved projects:", end=" ")
        for moved_project in moved_projects:
            print(f"'{moved_project}'", end=", ")
        print(f"to '{to_group}'.")

    if same_dst_projects:
        print("Projects:", end=" ")
        for same_dst_project in same_dst_projects:
            print(f"'{same_dst_project}'", end=", ")
        print(f"is already in '{to_group}'.")

    if locked_projects:
        print("Must unlock:", end=" ")
        for locked_project in locked_projects:
            print(f"'{locked_project}'", end=", ")
        print("before moving.")

    pass
