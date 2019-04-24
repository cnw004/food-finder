from .funcmodule import *
import click
import configparser

@click.group()
def main():
    """
    Simple CLI for finding restuarants nearby by Cole Whitley
    """
    pass

@main.command()
@click.option('--kind', default='food', help='Kind of business you are searching for (i.e. chinese, bbq, etc.)')
@click.argument('addr')
def find(addr, kind):
    """This function will find businesses nearby"""

    location = get_location(addr)
    if location == None:
        click.echo('Invalid address')
        exit(1)
    else:
        coordinates = (location.latitude, location.longitude)
        
    response = search_yelp(coordinates, kind)
    click.echo('latitude: ' + str(coordinates[0]) + ' longitude: ' + str(coordinates[1]))
    click.echo('categories: ' + kind)
    click.echo(response)

if __name__ == "__main__":
    main()