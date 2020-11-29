import click

from pygpg.key_owner import KeyOwner
from pygpg.enums.trust_value import TrustValue


TRUST_TO_COLOR = {
    TrustValue.UNKNOWN: "white",
    TrustValue.UNTRUSTED: "red",
    TrustValue.INVALID: "red",
    TrustValue.REVOKED: "red",
    TrustValue.EXPIRED: "yellow",
    TrustValue.MARGINAL: "magenta",
    TrustValue.FULL: "green",
    TrustValue.ULTIMATE: "blue",
    TrustValue.WELL_KNOWN: "yellow",
    TrustValue.ERROR: "yellow",
}


def display_key_owner(owner: KeyOwner):
    formatted_emails = [f"<{email}>" for email in owner.emails]
    click.echo(f"{owner.name} AKA {', '.join(formatted_emails)}")
    click.echo("Trust: ", nl=False)
    click.secho(owner.trust.name.lower(), fg=TRUST_TO_COLOR[owner.trust])
