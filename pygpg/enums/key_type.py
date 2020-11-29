from enum import Enum


class KeyType(Enum):
    PUBLIC_KEY = "pub"
    PRIVATE_KEY = "sec"
    SUBKEY = "sub"
    SECRET_SUBKEY = "ssb"
