import typer

from src.dpx.cli import create, read, update, delete, dev

app = typer.Typer()

app.add_typer(create.app)
app.add_typer(read.app)
app.add_typer(update.app)
app.add_typer(delete.app)
app.add_typer(dev.app, name="dev")

# __all__ = ["create", "read", "update", "delete"]
