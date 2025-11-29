from src.dpx.cli import app


@app.command()
def hello(name: str) -> None:
    print(f"Hello {name}!")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
