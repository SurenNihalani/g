"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """g."""


if __name__ == "__main__":
    main(prog_name="g")  # pragma: no cover
