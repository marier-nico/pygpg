"""This module contains the code for the ls wrapper command."""
import click


@click.command()
def ls():
    """Show a list of GPG keys in the keyring."""
    click.secho("ls", fg="green")
