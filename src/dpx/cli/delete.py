"""Delete CLI commands.

rm
"""

from typing_extensions import Annotated
import typer

app = typer.Typer()


@app.command()
def rm(
    project_names: Annotated[list[str], typer.Argument()],
    playground: Annotated[bool, typer.Option()],
    temps: Annotated[bool, typer.Option()],
) -> None:
    pass
