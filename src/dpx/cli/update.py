"""Update CLI commands.

rename
drename
uds
promote
demote
mv
"""

from typing_extensions import Annotated
from pathlib import Path

from rich import print
import typer

from src.dpx.cli.utils.util import Project, ProjectManager
from src.dpx.utils.paths import PROJECTS_DIR

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


# @app.command()
# def rename(
#     name_to_new: Annotated[str, typer.Argument()],
#     playground: Annotated[bool, typer.Option()] = False,
# ) -> None:
#     pass


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
