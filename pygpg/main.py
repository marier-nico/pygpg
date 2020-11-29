"""Main entrypoint for the CLI."""
from typing import Optional

import click
import gnupg

from pygpg.commands.ls import ls


@click.group()
@click.option("--gpg-home")
@click.pass_context
def main(ctx, gpg_home: Optional[str]):
    """A thin wrapper around GPG with friendlier command line options!"""
    gpg = gnupg.GPG(gnupghome=gpg_home) if gpg_home else gnupg.GPG()
    ctx.obj = gpg


main.add_command(ls)


if __name__ == "__main__":
    main()  # pylint: disable=E1120
