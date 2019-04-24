from geopy.geocoders import Nominatim
import requests
import json
import configparser

def get_location(addr):
    """
    Given an address as a string return (latitude, longitude)
    """
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    location = geolocator.geocode(addr)
    return location

def search_yelp(coordinates, kinds):
    """
    Given coordinates as a tuple and type, query yelp and return a json object
    """

    # get our API secrets
    parser = configparser.ConfigParser()
    parser.read('CONFIG.cfg')
    key = parser.get('api-access', 'key')
    client_id = parser.get('api-access', 'client_id')

    # tuple -> string separated by commas
    kind_string = ','.join(kinds)

    url = 'https://api.yelp.com/v3/businesses/search?'
    url += '&' + 'kinds=' + kind_string
    url += '&' + 'latitude=' + coordinates['latitude']
    url += '&' + 'longitude=' + coordinates['longitude']

    headers = {'Authorization': 'Bearer ' + key,
        'Content-Type': 'application/json'}
    r = requests.get(url, headers=headers)
    output = json.loads(r.text)
    return output