"""Contains functions to export GPG keys."""
import subprocess
from typing import List, Tuple

import gnupg

from pygpg.exceptions import KeyExportError


def export_secret_subkeys(gpg: gnupg.GPG, key_id: str) -> Tuple[str, str]:
    """Export the secret subkeys for a given GPG key.

    :param gpg: The GPG interface used by the gnupg library
    :param key_id: The ID of the key for which to export subkeys
    :return: The GPG private key block (stdout) and stderr
    """
    command = gpg.make_args(["--armor", "--export-secret-subkeys", key_id], None)
    command.remove("--fixed-list-mode")
    command.remove("--with-colons")
    return run_export_command(command, key_id)


def export_public_key(gpg: gnupg.GPG, key_id: str) -> Tuple[str, str]:
    """Export a GPG public key.

    :param gpg: The GPG interface used by the gnupg library
    :param key_id: The ID of the key for which to create a backup
    :return: The backed up key dats (stdout) and stderr
    """
    command = gpg.make_args(["--armor", "--export", key_id], None)
    command.remove("--fixed-list-mode")
    command.remove("--with-colons")
    return run_export_command(command, key_id)


def export_private_key(gpg: gnupg.GPG, key_id: str) -> Tuple[str, str]:
    """Export all necessary information about a key to restore it.

    From the GPG man pages:
    The exported data includes all data which is needed to restore the key or keys later with GnuPG.
    The format is basically the OpenPGP format but enhanced with GnuPG specific data.

    :param gpg: The GPG interface used by the gnupg library
    :param key_id: The ID of the key for which to create a backup
    :return: The backed up key dats (stdout) and stderr
    """
    command = gpg.make_args(["--armor", "--export-secret-keys", key_id], None)
    command.remove("--fixed-list-mode")
    command.remove("--with-colons")
    return run_export_command(command, key_id)


def run_export_command(command: List[str], key_id: str) -> Tuple[str, str]:
    """Run a command and handle errors in the context of an export.

    :param command: The command to execute
    :param key_id: The ID of the key that was exported
    :return: A tuple containing stdout and stderr
    """
    try:
        result = subprocess.run(command, shell=False, capture_output=True, check=True)
    except subprocess.CalledProcessError as ex:
        raise KeyExportError(key_id) from ex

    return result.stdout.decode("utf-8"), result.stderr.decode("utf-8")
