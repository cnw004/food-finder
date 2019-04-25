from geopy.geocoders import Nominatim
import requests
import simplejson as simplejson
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
    geolocator = Nominatim(user_agent="fp_cli")
    location = geolocator.geocode(addr)
    return location

def handle_error(radius, number):
    if radius > 40000:
        print('Radius too large. Please limit to <25.')
        exit(1)
    elif number > 50:
        print('Cannot return that many results. Please limit number to <50.')
        exit(1)

def search_yelp(coordinates, kinds, number, radius, json, sort, price):
    """
    Given coordinates as a tuple and type, query yelp and return a json object
    """

    # handle simple errors
    handle_error(int(radius), int(number))

    # get our API secrets
    parser = configparser.ConfigParser()
    parser.read('CONFIG.cfg')
    key = parser.get('api-access', 'key')

    headers = {'Authorization': 'Bearer ' + key,
        'Content-Type': 'application/json'}

    
    # build out the url with all search options
    url = 'https://api.yelp.com/v3/businesses/search?'
    url += '&' + 'term=food'
    url += '&' + 'latitude=' + coordinates['latitude']
    url += '&' + 'longitude=' + coordinates['longitude']
    url += '&' + 'limit=' + number
    url += '&' + 'radius=' + str(radius)
    url += '&' + 'sort_by' + sort
    # tuple -> string separated by commas
    if kinds != ():
        url += '&' + 'categories=' + ','.join(kinds)
    if price[0] != '0':
        url += '&' + 'price=' + ','.join(price)

    r = requests.get(url, headers=headers)
    dirty_output = simplejson.loads(r.text)
    #print(dirty_output)
    sanitized_output = simplejson.dumps(sanitize_data(dirty_output), indent=4 * ' ')
    if json:
        return sanitized_output
    else:
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
        desired_attrs = ['rating', 'is_closed', 'price', 'distance', 'phone', 'categories', 'location']
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
                elif item == 'location':
                    info[business['name']]['location'] = business['location']['address1'] + ', ' + business['location']['city']
                else:
                    info[business['name']][item] = business[item]
        
    return info

def pretty_print(sanitized_data):
    output_string = ''
    printer = simplejson.loads(sanitized_data)
    for name in printer:
        output_string += name + '\n'
        for info_item in printer[name]:
            output_string += '\t' + info_item + ': ' + str(printer[name][info_item]) + '\n'
        output_string += '\n'
    return output_string