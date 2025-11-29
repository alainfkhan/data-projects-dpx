"""Update CLI commands.

rename
drename
uds
promote
demote
mv
"""

from typing_extensions import Annotated

import typer

app = typer.Typer()


@app.command()
def rename(
    name_to_new: Annotated[str, typer.Argument()],
    playground: Annotated[bool, typer.Option()] = False,
) -> None:
    pass


@app.command()
def drename(
    name: Annotated[str, typer.Argument("-n")],
    dname_to_new: Annotated[list[str], typer.Argument()],
    ddir: Annotated[str, typer.Argument()],
    playground: Annotated[bool, typer.Option()] = False,
) -> None:
    pass


@app.command()
def uds(do_all: Annotated[bool, typer.Option()] = False) -> None:
    pass


@app.command()
def promote(name: Annotated[str, typer.Argument()]) -> None:
    pass


@app.command()
def demote(name: Annotated[str, typer.Argument()]) -> None:
    pass


@app.command()
def mv(name: Annotated[str, typer.Argument()]) -> None:
    pass
