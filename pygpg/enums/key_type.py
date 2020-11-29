"""Contains an enum to represent the different GPG key types."""
from enum import Enum


class KeyType(Enum):
    """Different possible types of GPG keys.

    Only a small subset of all possible types of records that can be returned by GPG are handled
    here. For a full list, see [this](https://github.com/gpg/gnupg/blob/master/doc/DETAILS#field-1---type-of-record).
    """

    PUBLIC_KEY = "pub"
    PRIVATE_KEY = "sec"
    SUBKEY = "sub"
    SECRET_SUBKEY = "ssb"
