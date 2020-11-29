"""Contains an enum to represent the different trust levels of a key or its owner."""
from __future__ import annotations
from enum import Enum


class TrustValue(Enum):
    """Different levels of trust for GPG keys or key owners.

    The trust value of a given key or key owner determines whether or not the entity in question is trusted, and if so,
    how trusted they are.

    This list is non-exhaustive. It does not handle the value "s" for keys, and does not handle
    any values related to sig records, such as [!, -, ?, %].

    Details for different values can be found
    [here](https://github.com/gpg/gnupg/blob/master/doc/DETAILS#field-2---validity).
    """

    UNKNOWN = {"o", "q", "-"}
    UNTRUSTED = {"n"}
    INVALID = {"i"}
    REVOKED = {"r"}
    EXPIRED = {"e"}
    MARGINAL = {"m"}
    FULL = {"f"}
    ULTIMATE = {"u"}
    WELL_KNOWN = {"w"}
    ERROR = {"?"}

    @staticmethod
    def from_symbol(symbol: str) -> TrustValue:
        """Get the enum variant that is associated with the given symbol.

        The symbol is the single letter that is used by GPG to identify trust levels.

        :param symbol: The symbol representing a given trust level
        :return: The variant of the TrustValue enum
        """
        for validity in TrustValue:
            if symbol in validity.value:
                return validity

        return TrustValue.ERROR
