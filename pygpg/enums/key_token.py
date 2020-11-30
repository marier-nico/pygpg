"""Contains the enum to represent different key tokens."""
from enum import Enum


class KeyToken(Enum):
    """Different possible key tokens.

    The key's token indicates if it is only a stub (because no secret key is present),
    or if the secret key is available.
    """

    STUB = "#"
    FULL = "+"
