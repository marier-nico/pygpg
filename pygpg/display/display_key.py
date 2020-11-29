"""Functions to display a GPG key under different formats."""
import click

from pygpg.gpg_key import GPGKey
from pygpg.enums.trust_value import TrustValue
from pygpg.display.trust_value_colors import TRUST_COLOR


def display_key_oneline(key: GPGKey, indent=""):
    """Display a GPG key on the terminal on a single line.

    :param key: The GPG key to display
    :param indent: Indentation to add before printing each key
    """
    key_type = key.key_type.name.lower().replace("_", " ").capitalize()
    click.echo(f"{indent}{key_type}: ", nl=False)
    click.secho(key.key_id, fg="cyan", nl=False)
    click.secho(f" Created: {key.creation_date.isoformat()}", fg="white", nl=False)

    if key.expiration_date and key.key_validity == TrustValue.EXPIRED:
        click.secho(f" Expired: {key.expiration_date.isoformat()}", fg="red", nl=False)
    else:
        if key.expiration_date:
            click.secho(f" Expires: {key.expiration_date.isoformat()}", fg="green", nl=False)

        click.secho(f" Trust: {key.key_validity.name.lower()}", fg=TRUST_COLOR[key.key_validity], nl=False)

    capabilities = [cap.name.lower().capitalize() for cap in key.key_capabilities] or "none"
    click.secho(f" Capabilities: {capabilities}", fg="bright_black")


def display_subkeys_oneline(key: GPGKey, indent=""):
    """Display a GPG key's subkeys with each subkey on a single line.

    :param key: The GPG key for which the subkeys should be shown
    :param indent: Indentation to add before printing each subkey
    """
    if key.subkeys:
        for subkey in key.subkeys:
            display_key_oneline(subkey, indent)
