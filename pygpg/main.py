import click


@click.command()
def main():
    click.secho("Hello, World!", fg="green")


if __name__ == "__main__":
    main()
