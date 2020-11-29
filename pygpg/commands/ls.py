"""This module contains the code for the ls wrapper command."""
from typing import Dict, List

import click

from pygpg.key_owner import KeyOwner
from pygpg.gpg_key import GPGKey
from pygpg.display.display_key import display_key_oneline, display_subkeys_oneline
from pygpg.display.display_key_owner import display_key_owner


@click.command()
@click.option("-a", "--all", "all_", is_flag=True, help="List all keys in the keyring, both public and private")
@click.option("-p", "--private", is_flag=True, help="List private keys in the keyring")
@click.option("-n", "--no-subkeys", is_flag=True, help="Omit subkeys in the list of shown keys")
@click.pass_obj
def ls(gpg, all_: bool, private: bool, no_subkeys: bool):  # pylint: disable=C0103
    """Show a list of GPG keys in the keyring."""
    public_keys = gpg.list_keys()
    private_keys = gpg.list_keys(True)

    if all_:
        keys_to_show = []
        keys_to_show.extend(public_keys)
        keys_to_show.extend(private_keys)
    elif private:
        keys_to_show = private_keys
    else:
        keys_to_show = public_keys

    owners_to_keys: Dict[KeyOwner, List[GPGKey]] = {}
    for key in keys_to_show:
        gpg_key = GPGKey.from_gpg_key_dict(key)
        if gpg_key.key_owner in owners_to_keys:
            owners_to_keys[gpg_key.key_owner].append(gpg_key)
        else:
            owners_to_keys[gpg_key.key_owner] = [gpg_key]

    for owner, public_keys in owners_to_keys.items():
        click.echo()
        display_key_owner(owner)
        click.echo()
        for key in public_keys:
            display_key_oneline(key, indent="\t")

            if key.subkeys and not no_subkeys:
                display_subkeys_oneline(key, indent="\t  ")
