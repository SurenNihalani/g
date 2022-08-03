"""Command-line interface."""
import click

from .shell import shell



cli = click.CommandCollection(sources=[shell])

def main():
    shell()


if __name__ == "__main__":
    main()