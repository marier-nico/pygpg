"""Contains a dataclass to represent a GPG key's owner."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Union
import re

from pygpg.enums.trust_value import TrustValue


@dataclass
class KeyOwner:
    """Contains data about a GPG key's owner."""

    name: str
    emails: List[str]
    trust: TrustValue

    def __key(self):
        return self.name, tuple(self.emails), self.trust

    def __hash__(self):
        return hash(self.__key())

    @staticmethod
    def from_gpg_key_dict(gpg_key_dict: Dict[str, Union[str, Dict]]) -> KeyOwner:
        """Create a KeyOwner instance from the dict returned by the gnupg library.

        :param gpg_key_dict: The dict returned by the gnupg library
        :return: An instance of KeyOwner with field values taken from the gnupg dict
        """
        uids = gpg_key_dict.get("uids")
        if not uids or len(uids) == 0:
            raise ValueError(f"This GPG key does not list any user IDs: {gpg_key_dict}")

        parsed_uids = []
        for uid in uids:
            match = re.search(r"([\w ]+)[^<]*<([^>]+)>", uid)
            if not match:
                raise ValueError(f"Could not parse the following key user ID: {uid}")

            name = match.group(1).strip()
            email = match.group(2).strip()
            parsed_uids.append((name, email))

        owner_trust = gpg_key_dict.get("ownertrust") or "?"
        if isinstance(owner_trust, str):
            return KeyOwner(
                name=parsed_uids[0][0],
                emails=[email for name, email in parsed_uids],
                trust=TrustValue.from_symbol(owner_trust),
            )

        raise RuntimeError(f"This GPG key's ownertrust was not a string: {gpg_key_dict}")
