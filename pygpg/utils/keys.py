from typing import List

import gnupg

from pygpg.gpg_key import GPGKey


def get_public_keys(gpg: gnupg.GPG) -> List[GPGKey]:
    public_keys = gpg.list_keys()

    return [GPGKey.from_gpg_key_dict(key) for key in public_keys]


def get_private_keys(gpg: gnupg.GPG) -> List[GPGKey]:
    private_keys = gpg.list_keys(True)

    return [GPGKey.from_gpg_key_dict(key) for key in private_keys]
