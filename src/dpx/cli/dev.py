import typer
from typing import Annotated

from icecream import ic

from src.dpx.cli.utils.util import Project, ProjectManager
from src.dpx.cli.utils.url_manager import URLDispatcher, KaggleHandler
from src.dpx.utils.paths import PROJECTS_DIR

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


@app.command()
def main() -> None:
    pass
