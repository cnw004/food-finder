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
@click.option('--kind', '-k', type=str, multiple=True, help='Kind of business you are searching for (i.e. chinese, bbq, etc.)')
@click.option('--number', '-n', type=int, default='5',help='Number of results that will be returned')
@click.option('--radius', '-r', type=int, default='2',help='Radial distance away you want to search')
@click.option('--json/--no-json', default=False, help='Flag allows for output to display as json')
@click.option('--sort', '-s', default='rating', type=click.Choice(['rating', 'best_match', 'distance']), help='Specify how you wish to sort results')
@click.option('--price', '-p', multiple=True, type=click.Choice(['1', '2', '3', '4']), help='Specify price point of restaurants')
@click.argument('addr')
def find(addr, kind, number, radius, json, sort, price):
    """Search for the best food nearby"""

    location = get_location(addr)
    if location == None:
        click.echo('Invalid address')
        exit(1)
    else:
        coordinates = {'latitude': str(location.latitude), 
                        'longitude': str(location.longitude)}
        
    response = search_yelp(coordinates, kind, str(number), miles_to_meters(radius), json, sort, price)
    #click.echo('latitude: ' + coordinates['latitude'] + ' longitude: ' + coordinates['longitude'])
    #click.echo('categories: ' + ','.join(kind))
    click.echo(response)
    

if __name__ == "__main__":
    main()