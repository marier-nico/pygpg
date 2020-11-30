"""This module contains the code for the renew wrapper command."""
import sys
import re
from typing import Optional

import click
import gnupg

from pygpg.utils.keys import get_private_keys
from pygpg.gnupg_extension.edit_key import edit_key
from pygpg.enums.trust_value import TrustValue
from pygpg.enums.key_token import KeyToken
from pygpg.gpg_key import GPGKey


def validate_valid_duration(_ctx, _param, value: str) -> str:
    value = value.strip()
    match = re.search(r"\d+[wmy]?$", value)
    if match:
        return value

    raise click.BadParameter("must be in the format specified in the command's help message")


def validate_key_id(ctx, _param, value: Optional[str]) -> Optional[GPGKey]:
    if value:
        value = value.strip()
        private_keys = get_private_keys(ctx.obj)
        supplied_key = [key for key in private_keys if key.key_id == value]

        if not supplied_key:
            raise click.BadParameter("must be a primary key")
        elif supplied_key[0].key_token == KeyToken.STUB:
            raise click.BadParameter("the private part of the supplied key must be available")

    return value


def prompt_for_key_id(gpg: gnupg.GPG) -> str:
    valid_private_keys = [key for key in get_private_keys(gpg) if key.key_token == KeyToken.FULL]
    for i, key in enumerate(valid_private_keys):
        expiration = key.expiration_date.isoformat() if key.expiration_date else "never"

        if key.expiration_date:
            expiration_color = "red" if key.key_validity == TrustValue.EXPIRED else "green"
        else:
            expiration_color = "yellow"

        click.secho(f"[{i + 1}] {key.key_id} ", fg="cyan", nl=False)
        click.secho(f"Expires: {expiration} ", fg=expiration_color, nl=False)
        click.echo("- ", nl=False)

        owner_emails = [f"<{email}>" for email in key.key_owner.emails]
        click.secho(f"{key.key_owner.name} {', '.join(owner_emails)}", fg="bright_black")

    selected_index = click.prompt("Please select a key ID to modify", type=int) - 1
    if 0 <= selected_index <= len(valid_private_keys) - 1:
        return valid_private_keys[selected_index].key_id

    click.secho("Please select a number from the list")
    sys.exit(1)


@click.command()
@click.option(
    "-k",
    "--key-id",
    callback=validate_key_id,
    help="The ID of the GPG key to edit. "
    "The key must be a primary key, and the secret key needs to be present in the keyring",
)
@click.option(
    "-a",
    "--all",
    "all_",
    is_flag=True,
    help="Set the expiration of all subkeys of the selected key to the same date as the primary key",
)
@click.argument("valid_duration", callback=validate_valid_duration)
@click.pass_obj
def renew(gpg: gnupg.GPG, key_id: Optional[str], all_: bool, valid_duration: str):
    """Renew a GPG key or otherwise change its expiration date.

    VALID_DURATION is the duration for which the GPG key will be valid after executing
    this command. Values need to be specified in the following format:

        \b
         0   = key does not expire
        <n>  = key expires in n days
        <n>w = key expires in n weeks
        <n>m = key expires in n months
        <n>y = key expires in n years
    """
    if not key_id:
        key_id = prompt_for_key_id(gpg)

    edit_key_commands = ["expire", valid_duration]

    if all_:
        gpg_key = [key for key in get_private_keys(gpg) if key.key_id == key_id][0]
        for i, _subkey in enumerate(gpg_key.subkeys):
            edit_key_commands.extend([f"key {i + 1}", "expire", valid_duration])

    edit_key_commands.append("save")
    edit_key(gpg, edit_key_commands, key_id)
