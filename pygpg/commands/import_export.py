"""This module contains the code for the import and export commands."""
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

import click
import gnupg


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
            result = gpg.import_keys(open_file.read()).count
        except UnicodeDecodeError:
            pass

        return result
