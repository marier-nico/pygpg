"""Utilities for handling GPG keys."""
from typing import List

import gnupg

from pygpg.enums.key_token import KeyToken
from pygpg.gpg_key import GPGKey


def get_public_keys(gpg: gnupg.GPG) -> List[GPGKey]:
    """Get a list of public keys in the keyring.

    :param gpg: The GPG interface used by the gnupg library
    :return: The list of public keys in the keyring
    """
    public_keys = gpg.list_keys()

    return [GPGKey.from_gpg_key_dict(key) for key in public_keys]


def get_private_keys(gpg: gnupg.GPG) -> List[GPGKey]:
    """Get a list of private keys in the keyring.

    :param gpg: The GPG interface used by the gnupg library
    :return: The list of private keys in the keyring
    """
    private_keys = gpg.list_keys(True)

    return [GPGKey.from_gpg_key_dict(key) for key in private_keys]


def get_full_private_keys(gpg: gnupg.GPG) -> List[GPGKey]:
    """Get a list of private keys with a full private part.

    GPG supports exporting only the subkeys for a given key, and in this case
    a stub of the primary private key is also exported (the stub). This stub
    cannot be used to do anything with the primary key, so it's useful to list
    only keys that can actually be used.

    :param gpg: The GPG interface used by the gnupg library
    :return: The list of fully available private keys in the keyring
    """

    return [key for key in get_private_keys(gpg) if key.key_token == KeyToken.FULL]
