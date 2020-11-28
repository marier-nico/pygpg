"""Main entrypoint for the CLI."""
import click

from pygpg.commands.ls import ls


@click.group()
def main():
    """A thin wrapper around GPG with friendlier command line options!"""


main.add_command(ls)
