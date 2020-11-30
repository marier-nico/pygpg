"""Utilities for handling GPG keys."""
from typing import List

import gnupg

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
