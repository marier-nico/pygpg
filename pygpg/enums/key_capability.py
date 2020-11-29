"""Contains an enum to represent the different GPG key capabilities."""
from enum import Enum


class KeyCapability(Enum):
    """Different possible key capabilities.

    A key's capability determines what actions can be taken with any given key.
    See the documentation [here](https://github.com/gpg/gnupg/blob/master/doc/DETAILS#field-12---key-capabilities)
    """

    ENCRYPT = "e"
    SIGN = "s"
    CERTIFY = "c"
    AUTHENTICATE = "a"
    UNKNOWN = "?"
