from .funcmodule import *
import click
import configparser

@click.group()
def main():
    """
    Simple CLI for finding restuarants nearby
    """
    pass

@main.command()
@click.option('--kind', '-k', type=str, default='food', multiple=True,help='Kind of business you are searching for (i.e. chinese, bbq, etc.)')
@click.argument('addr')
def find(addr, kind):
    """Search for the best food nearby"""

    location = get_location(addr)
    if location == None:
        click.echo('Invalid address')
        exit(1)
    else:
        coordinates = {'latitude': str(location.latitude), 
                        'longitude': str(location.longitude)}
        
    response = search_yelp(coordinates, kind)
    click.echo('latitude: ' + coordinates['latitude'] + ' longitude: ' + coordinates['longitude'])
    click.echo('categories: ' + ','.join(kind))
    click.echo(response)

if __name__ == "__main__":
    main()