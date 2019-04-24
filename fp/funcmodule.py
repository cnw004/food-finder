from geopy.geocoders import Nominatim
import requests
import simplejson as json
import configparser

def meters_to_miles(meters):
    """
    helper function to convert meters to miles
    """
    return round(float(meters) * 0.00062137,2)

def miles_to_meters(miles):
    return int(round(miles * 1609.344,2))

def get_location(addr):
    """
    Given an address as a string return (latitude, longitude)
    """
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    location = geolocator.geocode(addr)
    return location

def search_yelp(coordinates, kinds, number, radius):
    """
    Given coordinates as a tuple and type, query yelp and return a json object
    """

    # get our API secrets
    parser = configparser.ConfigParser()
    parser.read('CONFIG.cfg')
    key = parser.get('api-access', 'key')
    client_id = parser.get('api-access', 'client_id')

    

    url = 'https://api.yelp.com/v3/businesses/search?'
    url += '&' + 'term=food'
    url += '&' + 'latitude=' + coordinates['latitude']
    url += '&' + 'longitude=' + coordinates['longitude']
    url += '&' + 'limit=' + number
    url += '&' + 'radius=' + str(radius)
    url += '&' + 'sort_by' + 'rating'
    # tuple -> string separated by commas
    if kinds != ():
        kind_string = ','.join(kinds)
        url += '&' + 'categories=' + kind_string

    #print(url)

    headers = {'Authorization': 'Bearer ' + key,
        'Content-Type': 'application/json'}
    r = requests.get(url, headers=headers)
    dirty_output = json.loads(r.text)
    #print(dirty_output)
    sanitized_output = json.dumps(sanitize_data(dirty_output), sort_keys=True, indent=4 * ' ')
    pretty_string = pretty_print(sanitized_output)

    return pretty_string

def sanitize_data(raw_data):
    """
    Sanitize the json data that is returned from the HTTP request
    """
    info = {}
    for business in raw_data['businesses']:
        
        # the object we will store our information in, based on name
        info[business['name']] = {}

        # check each atrribute listed for each business and make sure we care about it, then add it to our info obj
        desired_attrs = ['rating', 'is_closed', 'price', 'distance', 'phone', 'categories']
        for item in desired_attrs:
            if item in business:
                if item == 'distance':
                    info[business['name']][item] = str(meters_to_miles(business[item])) + ' miles'
                elif item == 'categories':
                    category_list = []
                    for i in range(len(business['categories'])):
                        category_list.append(business['categories'][i]['title'])
                    info[business['name']][item] = ', '.join(category_list)
                elif item == 'is_closed':
                    info[business['name']]['open'] = (business['is_closed'] == False)
                else:
                    info[business['name']][item] = business[item]
        
    return info

def pretty_print(sanitized_data):
    output_string = ''
    printer = json.loads(sanitized_data)
    for name in printer:
        output_string += name + '\n'
        for info_item in printer[name]:
            output_string += '\t' + info_item + ': ' + str(printer[name][info_item]) + '\n'
        output_string += '\n'
    return output_string