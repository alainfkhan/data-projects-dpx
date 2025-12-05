import typer
from typing import Annotated

from icecream import ic

from src.dpx.cli.utils.util import Project, ProjectManager
from src.dpx.cli.utils.url_manager import URLDispatcher
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
def main() -> None:
    pass
