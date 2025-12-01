"""Delete CLI commands.

TODO: rm moves a project to trash, until deletion some days later

rm
"""

from typing_extensions import Annotated
import typer

app = typer.Typer()


@app.command()
def rm(
    names: Annotated[list[str], typer.Argument()],
    group: Annotated[str, typer.Option()] = "main",
    playground: Annotated[bool, typer.Option()] = False,
    temps: Annotated[bool, typer.Option()] = False,
    all_temps: Annotated[bool, typer.Option()] = False,
) -> None:
    """Delete projects."""
    pass
