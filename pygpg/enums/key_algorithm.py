from __future__ import annotations
from enum import Enum


class PublicKeyAlgorithm(Enum):
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
        for algo in PublicKeyAlgorithm:
            if algo and algo_id in algo.value:
                return algo

        return PublicKeyAlgorithm.UNKNOWN
