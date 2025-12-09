"""Create CLI commands only

TODO: finish init

init
dl
cdb
dpromote
"""

from typing_extensions import Annotated

import typer
from icecream import ic
from rich import print

from src.dpx.cli.utils.util import ProjectManager, Project
from src.dpx.utils.paths import PROJECTS_DIR
from src.dpx.utils.util import (
    temp_prefix,
    copy_attachment,
    random_string,
)

doptions: list[str] = ["ripe", "metal"]
# data folder name options
# ripe means raw, interim, processed, external
# metal means bronze, silver, gold, external

base_ddir = "r"
default_doption = "ripe"
current_main = "main"

app = typer.Typer()
# projects_manager = ProjectManager()


@app.command(help="Download a dataset to an existing project.")
def dl(
    name: Annotated[
        str,
        typer.Argument(help="The name of the project."),
    ],
    url: Annotated[
        str,
        typer.Option(
            "-u",
            "--url",
            help="The url source of the dataset.",
        ),
    ],
    playground: Annotated[
        bool,
        typer.Option(
            "-p",
            "--playground",
            help="Download to a project in playground.",
        ),
    ] = False,
    group: Annotated[
        str,
        typer.Option(
            "-g",
            "--group",
            help="The group of the project.",
        ),
    ] = current_main,
) -> None:
    # Case where url is necessary
    # Maybe possible to download data not using url
    if not url:
        raise ValueError("Must have a url.")

    # Necessary
    projects_manager = ProjectManager()

    projects_manager.verify_group(group)
    projects_manager.verify_project(name)

    if playground:
        group = "playground"

    this_project_path = PROJECTS_DIR / group / name

    project = Project(this_project_path)

    if url:
        project.handle_url(url)
        project.append_source(url)


# @app.command()
# def dpromote(
#     name: Annotated[str, typer.Argument()],
#     playground: Annotated[bool, typer.Option()] = False,
#     ddir: Annotated[str, typer.Option()] = base_ddir,
#     ca: Annotated[str, typer.Option()] = copy_attachment,
# ) -> None:
#     pass


# @app.command("Create a database")
# def cdb(
#     name: Annotated[str, typer.Argument()],
#     dbn: Annotated[str, typer.Option()] = temp_prefix + random_string(),
# ) -> None:
#     pass


@app.command(help="Initialise a project workspace in an existing project group.")
def init(
    *,
    name: Annotated[
        str,
        typer.Argument(
            help="The name of the project you want to initialise.",
        ),
    ] = temp_prefix + random_string(),
    playground: Annotated[
        bool,
        typer.Option(
            "-p",
            "--playground",
            help="Initialise a project in playground.",
        ),
    ] = False,
    group: Annotated[
        str,
        typer.Option(
            "-g",
            "--g",
            help="Initialise a project in group.",
        ),
    ] = current_main,
    # doption: Annotated[str, typer.Option()] = doption,
    url: Annotated[
        str | None,
        typer.Option(
            "-u",
            "--url",
        ),
    ] = None,
    force: Annotated[
        bool,
        typer.Option("-f", "--force", help="Force overwrite."),
    ] = False,
) -> None:
    """Initialises a workspace.

    dpx init smith-somedataset
        Initialise a workspace called 'smith-somedataset' in the main group.

    dpx init smith-somedataset -url <url> -g <group>
        Initialise a project called 'smith-somedataset'
        with data downloaded from <url>
        in group <group>
    """

    project_manager = ProjectManager()
    project_manager.verify_group(group)

    if not project_manager.can_create_project(name):
        raise ValueError(f"Project '{name}' cannot be created.")

    if playground:
        group = "playground"

    this_project_path = PROJECTS_DIR / group / name
    this_project_path.mkdir(exist_ok=True)

    # make data folders
    project = Project(this_project_path)
    project.mkdir_data_folders()

    # make other init folders
    project.mkdir_other_files()

    project.lock()

    print(f"Initialised new project: '{name}' in group: '{group}'.")

    if not url:
        return

    # Dowload data using cli command
    dl(
        name=name,
        url=url,
        playground=playground,
        group=group,
    )
