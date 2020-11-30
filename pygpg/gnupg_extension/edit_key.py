"""Contains a function which allows editing a GPG key non-interactively."""
import subprocess
from typing import List, Tuple

import gnupg

from pygpg.exceptions import KeyEditError


def edit_key(gpg: gnupg.GPG, commands: List[str], key_id: str) -> Tuple[str, str]:
    """Edit a given GPG key's attributes.

    This function extends the functionality provided by the gnupg library, because
    it does not allow changing key attributes. The only way to do this (it seems) is
    to tell the GPG binary to read from standard input and to pipe a string to it.

    This string represents the series of commands that would normally be run interactively,
    which is far from ideal, but it does appear to be the only option to allow key editing.
    The string in question is automatically created from the supplied commands.

    :param gpg: The GPG interface used by the gnupg library
    :param commands: The list of commands to execute during the edit. These commands
                     should be the same as what would be entered in the interactive
                     menu produced by `gpg --edit-key {key_id}`.
    :param key_id: The ID of the key to edit
    :return: A tuple formed with (stdout, stderr), with both streams as strings
    """
    command = gpg.make_args(["--command-fd", "0", "--edit-key", key_id], None)
    command.remove("--fixed-list-mode")
    command.remove("--with-colons")
    full_edit_command_string = "\n".join(commands) + "\n"

    try:
        result = subprocess.run(
            command, shell=False, input=full_edit_command_string.encode("utf-8"), capture_output=True, check=True
        )
    except subprocess.CalledProcessError as ex:
        raise KeyEditError(key_id) from ex

    return result.stdout.decode("utf-8"), result.stderr.decode("utf-8")
