import typer
from typing import Annotated

from icecream import ic

from src.dpx.cli.util import FileManager
from src.dpx.utils.paths import PROJECTS_DIR

app = typer.Typer()

test_project = "test"
test_project_path = PROJECTS_DIR / "main" / test_project
fm = FileManager(test_project_path)


@app.command()
def hello(name: Annotated[str, typer.Argument()]) -> None:
    print(f"hello {name}")
    pass


@app.command()
def main() -> None:
    x = fm.other_files_structure.items()
    ic(x)

    for name, subtree in x:
        ic(name)
        ic(subtree)

    pass
