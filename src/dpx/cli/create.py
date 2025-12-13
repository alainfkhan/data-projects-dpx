"""Create CLI commands only

TODO: finish init

init
cdb
"""

import os
import warnings
from typing_extensions import Annotated

import typer
from icecream import ic
from rich import print

from src.dpx.cli.utils.util import ProjectManager, Project
from src.dpx.utils.paths import PROJECTS_DIR
from src.dpx.utils.util import temp_prefix, copy_attachment, random_string, csv_to_excel

doptions: list[str] = ["ripe", "metal"]
# data folder name options
# ripe means raw, interim, processed, external
# metal means bronze, silver, gold, external

base_ddir = "r"
default_doption = "ripe"
current_main = "main"

default_save_to = "interim"

# Help default descriptions:
# TODO: add app conf for all help descriptions + other
name_help = "The name of the project."
url_help = "The url source of the dataset."
playground_help = "Choose the playground group."
group_help = "The name of the group."
force_overwrite_help = "Force overwrite."

app = typer.Typer()
# projects_manager = ProjectManager()


@app.command(help="Create a new group.")
def gadd(
    group: Annotated[
        str,
        typer.Argument(help="The name of the group you want to create."),
    ],
) -> None:
    project_manager = ProjectManager()
    project_manager.create_group(group)


@app.command(help="Download a dataset to an existing project.")
def dl(
    name: Annotated[
        str,
        typer.Argument(help=name_help),
    ],
    url: Annotated[
        str,
        typer.Option(
            "-u",
            "--url",
            help=url_help,
        ),
    ],
    playground: Annotated[
        bool,
        typer.Option(
            "-p",
            "--playground",
            help=playground_help,
        ),
    ] = False,
    group: Annotated[
        str,
        typer.Option(
            "-g",
            "--group",
            help=group_help,
        ),
    ] = current_main,
) -> None:
    # Case where url is necessary
    # Maybe possible to download data not using url
    if not url:
        raise ValueError("Must have a url.")

    if playground:
        group = "playground"

    projects_manager = ProjectManager()
    projects_manager.verify_group(group)
    projects_manager.verify_project(name)

    this_project_path = PROJECTS_DIR / group / name
    project = Project(this_project_path)

    if url:
        project.handle_url(url)
        project.append_source(url)


@app.command(help="Copies all data in raw to interim in a project.")
def dcp(
    name: Annotated[
        str,
        typer.Argument(
            help=name_help,
        ),
    ],
    playground: Annotated[
        bool,
        typer.Option(
            "-p",
            "--playground",
            help=playground_help,
        ),
    ] = False,
    group: Annotated[
        str,
        typer.Option(
            "-g",
            "--group",
            help=group_help,
        ),
    ] = current_main,
    force_overwrite: Annotated[
        bool,
        typer.Option(
            "-f",
            "--force",
            help=force_overwrite_help,
        ),
    ] = False,
) -> None:
    """Copies all data in raw to interim in a project."""

    if playground:
        group = "playground"

    project_manager = ProjectManager()
    project_manager.verify_group(group)
    project_manager.verify_project(name)

    this_project_path = PROJECTS_DIR / group / name
    project = Project(this_project_path)

    created_copies = project.data_copy(force_overwrite)

    for created_copy in created_copies:
        print(f"'{created_copy.name}' created in '{created_copy.parent.parent.name}/{created_copy.parent.name}'")
        return

    warnings.warn("No files copied.")


@app.command(help="Initialise raw files.")
def dpromote(
    name: Annotated[
        str,
        typer.Argument(
            help=name_help,
        ),
    ],
    playground: Annotated[
        bool,
        typer.Option(
            "-p",
            "--playground",
            help=playground_help,
        ),
    ] = False,
    group: Annotated[
        str,
        typer.Option(
            "-g",
            "--group",
            help=group_help,
        ),
    ] = current_main,
    force_overwrite: Annotated[
        bool,
        typer.Option(
            "-f",
            "--force",
            help=force_overwrite_help,
        ),
    ] = False,
    # ddir: Annotated[str, typer.Option()] = base_ddir,
    # ca: Annotated[str, typer.Option()] = copy_attachment,
) -> None:
    """Copies and converts all .csv to .xlsx files from raw to interim."""

    if playground:
        group = "playground"

    project_manager = ProjectManager()
    project_manager.verify_project(name)
    project_manager.verify_group(group)

    this_project_path = PROJECTS_DIR / group / name
    project = Project(this_project_path)

    # Copy files from raw to interim
    dcp(
        name=name,
        playground=playground,
        group=group,
        force_overwrite=force_overwrite,
    )

    # Turn all .csv in raw to .xlsx in interim
    interim_files = os.listdir(project.data_interim_path)
    interim_file_paths = [project.data_interim_path / interim_file for interim_file in interim_files]

    for interim_file_path in interim_file_paths:
        stem, ext = os.path.splitext(interim_file_path.name)

        if ext not in [".csv"]:
            continue

        # TODO: assumes excel ext is always .xlsx
        supposed_xlsx_file = interim_file_path.parent / f"{stem}.xlsx"

        if supposed_xlsx_file.exists():
            if not force_overwrite:
                continue

        created_xlsx_filename = csv_to_excel(interim_file_path)
        print(
            f"'{created_xlsx_filename.name}' created in '{interim_file_path.parent.parent.name}/{interim_file_path.parent.name}'"
        )

    return


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
            help=name_help,
        ),
    ] = temp_prefix + random_string(),
    playground: Annotated[
        bool,
        typer.Option(
            "-p",
            "--playground",
            help=playground_help,
        ),
    ] = False,
    group: Annotated[
        str,
        typer.Option(
            "-g",
            "--g",
            help=group_help,
        ),
    ] = current_main,
    # doption: Annotated[str, typer.Option()] = doption,
    url: Annotated[
        str | None,
        typer.Option(
            "-u",
            "--url",
            help=url_help,
        ),
    ] = None,
    force_overwrite: Annotated[
        bool,
        typer.Option(
            "-f",
            "--force",
            help=force_overwrite_help,
        ),
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

    def end_message() -> None:
        print(f"Initialised new project: '{name}' in group: '{group}'.")
        pass

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

    project.add_final_excel_file()

    if not url:
        end_message()
        return

    # Dowload data using cli command
    print("Downloading files from URL...")
    dl(
        name=name,
        url=url,
        playground=playground,
        group=group,
    )

    print("Initialising downloaded files...")
    dpromote(
        name=name,
        playground=playground,
        group=group,
        force_overwrite=force_overwrite,
    )

    end_message()
