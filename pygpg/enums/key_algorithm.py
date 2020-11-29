"""Contains an enum to represent the different algorithms used by GPG."""
from __future__ import annotations
from enum import Enum


class PublicKeyAlgorithm(Enum):
    """Different algorithms used by GPG to create public keys.

    This list is non-exhaustive and contains only the values from
    [RFC 4880](https://tools.ietf.org/html/rfc4880#section-9.1), except for ED25519,
    which is not in the standard, but supported by GPG.
    """

    RSA = {1, 2, 3}
    ELGAMAL = {16}
    DSA = {17}
    ELLIPTIC_CURVE = {18}
    ECDSA = {19}
    DIFFIE_HELLMAN = {21}
    ED25519 = {22}
    UNKNOWN = None

    @staticmethod
    def from_algo_id(algo_id: int) -> PublicKeyAlgorithm:
        """Get the enum variant that is associated with the given algorithm ID.

        :param algo_id: The algorithm ID for which to get the algorithm in the enum
        :return: The variant of the PublicKeyAlgorithm enum
        """
        for algo in PublicKeyAlgorithm:
            if algo and algo_id in algo.value:
                return algo

        return PublicKeyAlgorithm.UNKNOWN
