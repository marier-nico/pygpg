"""Functions to display a GPG key's owner."""
import click

from pygpg.key_owner import KeyOwner
from pygpg.display.trust_value_colors import TRUST_COLOR


def display_key_owner(owner: KeyOwner):
    """Display the information about a GPG key's owner on the terminal.

    :param owner: The GPG key's owner
    """
    formatted_emails = [f"<{email}>" for email in owner.emails]
    click.echo(f"{owner.name} AKA {', '.join(formatted_emails)}")
    click.echo("Trust: ", nl=False)
    click.secho(owner.trust.name.lower(), fg=TRUST_COLOR[owner.trust])
