import click


from pygpg.gpg_key import GPGKey
from pygpg.enums.trust_value import TrustValue


UNTRUSTED_MESSAGE = "You do not trust this key"
TRUSTED_MESSAGE = "You trust this key"

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


def display_key(key: GPGKey, indent=""):
    key_type = key.key_type.name.lower().replace("_", " ").capitalize()
    click.echo(f"{indent}{key_type}: ", nl=False)
    click.secho(key.key_id, fg="cyan", nl=False)
    click.secho(f" Created: {key.creation_date.isoformat()}", fg="white", nl=False)

    if key.key_validity == TrustValue.EXPIRED:
        click.secho(f" Expired: {key.expiration_date.isoformat()}", fg="red", nl=False)
    else:
        if key.expiration_date:
            click.secho(f" Expires: {key.expiration_date.isoformat()}", fg="green", nl=False)

        click.secho(f" Trust: {key.key_validity.name.lower()}", fg=TRUST_COLOR[key.key_validity], nl=False)

    capabilities = [cap.name.lower().capitalize() for cap in key.key_capabilities] or "none"
    click.secho(f" Capabilities: {capabilities}", fg="bright_black")


def display_subkeys(key: GPGKey, indent=""):
    if key.subkeys:
        for subkey in key.subkeys:
            display_key(subkey, indent)


