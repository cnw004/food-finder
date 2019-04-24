from .funcmodule import *
import click


@click.command()
@click.option('--count', default=5, help='Number of options you want displayed.')
@click.option('--type', default='any',
              help='The type of food you are looking for.')
def main(count, type):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in range(count):
        click.echo('Searching for %s food!' % type)

if __name__ == "__main__":
    main()