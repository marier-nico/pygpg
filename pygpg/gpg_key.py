from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Dict, Union
from datetime import date, datetime

from pygpg.enums.key_algorithm import PublicKeyAlgorithm
from pygpg.enums.key_type import KeyType
from pygpg.enums.trust_value import TrustValue
from pygpg.enums.key_capability import KeyCapability
from pygpg.key_owner import KeyOwner


ISO_FORMAT = "%Y%m%dT%H%M%S"


@dataclass
class GPGKey:
    """Class for holding the information about a GPG key."""

    key_id: str
    key_owner: KeyOwner
    key_type: KeyType
    key_validity: TrustValue
    key_capabilities: List[KeyCapability]
    key_fingerprint: Optional[str]
    creation_date: date
    expiration_date: Optional[date]
    public_key_algorithm: Optional[PublicKeyAlgorithm]
    subkeys: List[GPGKey]

    @staticmethod
    def from_gpg_key_dict(gpg_key_dict: Dict[str, Union[str, Dict]]) -> GPGKey:
        key_id = gpg_key_dict["keyid"]
        key_owner = KeyOwner.from_gpg_key_dict(gpg_key_dict)
        key_type = KeyType(gpg_key_dict["type"])
        key_validity = TrustValue.from_symbol(gpg_key_dict["trust"])
        key_capabilities = list({KeyCapability(cap.lower()) for cap in gpg_key_dict["cap"]})
        key_fingerprint = gpg_key_dict.get("fingerprint")

        if "T" in gpg_key_dict["date"]:
            creation_date = datetime.strptime(gpg_key_dict["date"], ISO_FORMAT).date()
        else:
            creation_date = datetime.fromtimestamp(int(gpg_key_dict["date"])).date()

        if gpg_key_dict["expires"]:
            if "T" in gpg_key_dict["expires"]:
                expiration_date = datetime.strptime(gpg_key_dict["expires"], ISO_FORMAT).date()
            else:
                expiration_date = datetime.fromtimestamp(int(gpg_key_dict["expires"])).date()
        else:
            expiration_date = None

        if gpg_key_dict["algo"]:
            public_key_algorithm = PublicKeyAlgorithm.from_algo_id(int(gpg_key_dict["algo"]))
        else:
            public_key_algorithm = None

        subkeys = []
        if gpg_key_dict.get("subkeys"):
            for _subkey_id, subkey in gpg_key_dict["subkey_info"].items():
                subkey["uids"] = gpg_key_dict["uids"]
                subkey["ownertrust"] = gpg_key_dict["ownertrust"]
                subkeys.append(GPGKey.from_gpg_key_dict(subkey))

        return GPGKey(
            key_id=key_id,
            key_owner=key_owner,
            key_type=key_type,
            key_validity=key_validity,
            key_capabilities=key_capabilities,
            key_fingerprint=key_fingerprint,
            creation_date=creation_date,
            expiration_date=expiration_date,
            public_key_algorithm=public_key_algorithm,
            subkeys=subkeys
        )
