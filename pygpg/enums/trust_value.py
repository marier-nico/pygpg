from __future__ import annotations
from enum import Enum


class TrustValue(Enum):
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
        for validity in TrustValue:
            if symbol in validity.value:
                return validity

        return TrustValue.ERROR
