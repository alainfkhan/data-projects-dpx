"""Read CLI commands

ls
dls
head
tail
begin
open
"""

from typing_extensions import Annotated

import typer

ide = "code"
ides = ["code", "vim"]

app = typer.Typer()


@app.command()
def ls(
    playground: Annotated[bool, typer.Option()] = False,
    temps: Annotated[bool, typer.Option()] = False,
    show_all: Annotated[bool, typer.Option()] = False,
) -> None:
    pass


@app.command()
def dls(
    name: Annotated[str, typer.Argument()],
    playground: Annotated[bool, typer.Option()],
    ddir: Annotated[str, typer.Option()],
    ddirs: Annotated[list[str], typer.Option()],
) -> None:
    pass


@app.command()
def head(
    name: Annotated[str, typer.Argument()],
    playground: Annotated[bool, typer.Option()] = False,
    number: Annotated[int, typer.Option()] = 10,
) -> None:
    pass


@app.command()
def tail(
    name: Annotated[str, typer.Argument()],
    playground: Annotated[bool, typer.Option()] = False,
    number: Annotated[int, typer.Option()] = 10,
) -> None:
    pass


@app.command()
def begin(
    name: Annotated[str, typer.Argument()],
    playground: Annotated[bool, typer.Option()],
    ide: Annotated[str, typer.Option] = ide,
) -> None:
    pass


@app.command()
def open(
    name: Annotated[str, typer.Argument()],
    playground: Annotated[bool, typer.Option()],
    ddir: Annotated[str, typer.Argument()],
    dname: Annotated[str, typer.Argument()],
) -> None:
    pass
