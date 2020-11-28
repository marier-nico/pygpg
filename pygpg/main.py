"""Main entrypoint for the CLI."""
import click


@click.command()
def main():
    """Main command to invoke with the CLI."""
    click.secho("Hello, World!", fg="green")


if __name__ == "__main__":
    main()
