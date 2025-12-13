import os
import subprocess
import typer
from typing import Annotated

from icecream import ic

from src.dpx.cli.utils.util import Project, ProjectManager
from src.dpx.cli.utils.url_manager import URLDispatcher, KaggleHandler
from src.dpx.utils.paths import PROJECTS_DIR, DPX_DIR

app = typer.Typer()

test_project = "test"
test_project_path = PROJECTS_DIR / "main" / test_project
fm = Project(test_project_path)
pm = ProjectManager()


@app.command()
def hello(name: Annotated[str, typer.Argument()]) -> None:
    print(f"hello {name}")
    pass


@app.command()
def clean() -> None:
    pass
    name = "shaihid-yt"
    group = "main"
    url = "https://www.kaggle.com/datasets/kanchana1990/crypto-volatility-2025-bitcoin-and-memecoin-bull-run/discussion?sort=hotness"

    this_project_path = PROJECTS_DIR / group / name
    project = Project(this_project_path)

    kaggle_handler = KaggleHandler()
    handle = kaggle_handler.get_handle_from_url(url)
    print(handle)


@app.command(help="Create an empty excel file in data/processed/")
def finalxl(
    name: Annotated[
        str,
        typer.Argument(
            help="The name of the project.",
        ),
    ],
) -> None:
    project_manager = ProjectManager()
    project_manager.verify_project(name)

    group = project_manager.get_group_from_project(name)

    this_project_path = PROJECTS_DIR / group / name
    project = Project(this_project_path)

    project.add_final_excel_file()


@app.command(help="Change directory to a project.")
def cd(
    name: Annotated[str | None, typer.Argument()] = None,
) -> None:
    project_manager = ProjectManager()

    ic(name)
    if name is None:
        goto = DPX_DIR
        ic(goto)
    else:
        group = project_manager.get_group_from_project(name)
        goto = PROJECTS_DIR / group / name
        ic(goto)

    # subprocess.run(["cd", goto])
    os.chdir(goto)


@app.command()
def test_function(name: Annotated[str, typer.Argument()]) -> None:
    print(f"hello {name}")


@app.command()
def main() -> None:
    pass
