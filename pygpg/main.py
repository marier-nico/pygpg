"""Main entrypoint for the CLI."""
import sys
from typing import Optional

import click
import gnupg

from pygpg.commands.ls import ls
from pygpg.commands.renew import renew


@click.group()
@click.option(
    "--gpg-home",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    envvar="GPG_HOME",
    help="Path to the GPG home directory",
)
@click.option(
    "--gpg-binary",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    envvar="GPG_BINARY",
    help="Path to the GPG executable",
)
@click.option(
    "--use-agent",
    is_flag=True,
    envvar="USE_AGENT",
    help="Ask the GPG binary to use an in-memory GPG agent to remember credentials",
)
@click.option(
    "--keyring",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    envvar="KEYRING",
    help="Path to the GPG keyring file to use",
)
@click.pass_context
def main(
    ctx, gpg_home: Optional[click.Path], gpg_binary: Optional[click.Path], use_agent: bool, keyring: Optional[str]
):
    """A thin wrapper around GPG with friendlier command line options!"""
    gpg = gnupg.GPG() if gpg_home else gnupg.GPG()

    if gpg_home:
        gpg.gnupghome = str(gpg_home)
    if gpg_binary:
        gpg.gpgbinary = str(gpg_binary)
    if use_agent:
        gpg.use_agent = use_agent
    if keyring:
        gpg.keyring = keyring

    ctx.obj = gpg

    try:
        gpg.list_keys()  # Test that the GPG executable is usable
    except OSError as ex:
        click.secho(str(ex), fg="red")
        sys.exit(1)


main.add_command(ls)
main.add_command(renew)


if __name__ == "__main__":
    main()  # pylint: disable=E1120
