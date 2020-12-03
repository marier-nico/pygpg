"""This module contains the code for the import and export commands."""
import shutil
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional, Tuple

import click
import gnupg

from pygpg.gnupg_extension.export_key import export_private_key, export_public_key, export_secret_subkeys


@click.command("import")
@click.argument("file", type=click.Path(exists=True, readable=True, resolve_path=True))
@click.pass_obj
def import_key(gpg: gnupg.GPG, file: str):
    """Import one or many GPG keys.

    FILE can be an archive, directory, or individual key file.
    If FILE is a directory or an archive, all keys contained within
    will be imported. In the case of an archive, the keys must be
    at the top level of the archive (not in a directory in the archive).
    """
    path = Path(file)
    if path.is_dir():
        import_keys_in_dir(gpg, path)
        return

    imported_keys = import_key_from_file(gpg, path)
    if imported_keys:
        click.secho(f"Imported {imported_keys} key{'s' if imported_keys > 1 or imported_keys == 0 else ''}", fg="green")
        return

    with TemporaryDirectory() as temp_dir:
        try:
            shutil.unpack_archive(path, temp_dir)
            import_keys_in_dir(gpg, Path(temp_dir))
        except ValueError:
            click.secho("The archive extension is not known, keys cannot be extracted", fg="red")


def import_keys_in_dir(gpg: gnupg.GPG, dir_path: Path):
    """Import all the GPG keys in a directory.

    :param gpg: The GPG interface used by the gnupg library
    :param dir_path: The path to the directory from which to import keys
    """
    files = [file for file in dir_path.glob("*") if file.is_file()]

    total_count = 0
    for file in files:
        total_count += import_key_from_file(gpg, file)

    click.secho(f"Imported {total_count} key{'s' if total_count > 1 or total_count == 0 else ''}", fg="green")


def import_key_from_file(gpg: gnupg.GPG, file: Path) -> int:
    """Import GPG keys from a file.

    :param gpg: The GPG interface used by the gnupg library
    :param file: The file from which to import keys
    :return:
    """
    with open(file, "r") as open_file:
        result = 0
        try:
            result = gpg.import_keys(open_file.read(), extra_args=["--import-options", "restore"]).count
        except UnicodeDecodeError:
            pass

        return result


@click.command("export-subkeys")
@click.argument("key_id", nargs=-1)
@click.option("-o", "--output", type=click.Path(exists=False), help="Save the exported subkeys to this file")
@click.pass_obj
def export_subkeys(gpg: gnupg.GPG, output: Optional[str], key_id: Tuple[str]):
    """Export the private subkeys of one or many primary keys.

    KEY_ID is the ID of the primary key for which to export the secret subkeys.
    You can specify multiple IDs at once.

    The intended use for this command is to export secret subkeys before deleting
    the primary private key and re-importing the secret subkeys. This allows using
    the subkeys without having the primary private key on the system and allows for
    more security (by storing the primary private key somewhere else).

    In this situation, GPG exports a stub of the primary private key along with the
    subkeys, so note that this will not be importable by any other OpenPGP implementation.

    NOTE: If you want to backup keys, see the `backup` command.
    """
    if output and Path(output).exists():
        click.secho("A file already exists at this path, aborting to avoid overwriting", fg="red")
        sys.exit(1)

    all_output = []
    for key in key_id:
        private_key, _err = export_secret_subkeys(gpg, key)
        all_output.append(private_key)

    if output:
        with open(output, "w") as file:
            file.write("\n".join(all_output))
    else:
        click.echo("\n".join(all_output))


@click.command()
@click.argument("key_id", nargs=-1)
@click.option("-p", "--private", is_flag=True, help="Export a private key instead of a public key")
@click.option("-o", "--output", type=click.Path(exists=False), help="Save the exported keys to this file")
@click.pass_obj
def export(gpg: gnupg.GPG, output: Optional[str], private: bool, key_id: Tuple[str]):
    """Export one or many GPG keys.

    KEY_ID is the ID of the primary key that we want to export.
    You can specify multiple IDs at once.
    """
    if output and Path(output).exists():
        click.secho("A file already exists at this path, aborting to avoid overwriting", fg="red")
        sys.exit(1)

    all_output = []
    for key in key_id:
        if private:
            export_output, _err = export_private_key(gpg, key)
        else:
            export_output, _err = export_public_key(gpg, key)
        all_output.append(export_output)

    if output:
        with open(output, "w") as file:
            file.write("\n".join(all_output))
    else:
        click.echo("\n".join(all_output))
