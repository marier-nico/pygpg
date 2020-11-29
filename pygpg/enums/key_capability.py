from enum import Enum


class KeyCapability(Enum):
    ENCRYPT = "e"
    SIGN = "s"
    CERTIFY = "c"
    AUTHENTICATE = "a"
