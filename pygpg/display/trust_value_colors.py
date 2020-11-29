"""Contains a mapping to assign a color to a given TrustValue enum variant."""
from pygpg.enums.trust_value import TrustValue


TRUST_COLOR = {
    TrustValue.UNKNOWN: "yellow",
    TrustValue.UNTRUSTED: "red",
    TrustValue.INVALID: "red",
    TrustValue.REVOKED: "red",
    TrustValue.EXPIRED: "yellow",
    TrustValue.MARGINAL: "magenta",
    TrustValue.FULL: "green",
    TrustValue.ULTIMATE: "blue",
    TrustValue.WELL_KNOWN: "green",
    TrustValue.ERROR: "red",
}
