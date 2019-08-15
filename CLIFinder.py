from CollegeApps import *
from utils.scraper import *

import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

handler = logging.FileHandler('CollegeApartmentScraper.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)

def input_for_college():

    '''
    Used to find apartments with Wi-Fi around a single college
    '''

    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

    print('\n\n\n')

    college_name = input('College Name (required): ')
    college_location = input('City (required): ')
    state = input('State abbreviation (required): ').lower()

    while state.upper() not in states:

        state = input('State abbreviation (required): ').lower()


    enrollment = input('Enrollment: ')
    try:
        enrollment = int(enrollment)
    except ValueError:
        enrollment = 0

    address = input('Address: ')
    if len(address) == 0:

        address = None

    lat = input('Latitude of the point on campus you want to search around: ')
    try:
        lat = float(lat)
    except ValueError:
        lat = None

    lon = input('Longitude of the point on campus you want to search around: ')
    try:
        lon = float(lon)
    except ValueError:
        lon = None

    print('\n\n\nGetting apartments for {0}\n\n\n----------\n\n\n'.format(college_name))

    college = College(college_name=college_name, enrollment=enrollment, college_location=college_location, state=state, address=address, lat=lat, lon=lon)

    app_classes = college.find_apartments()

    print('{0} apartment complexes saved to an excel file at Excels/{1}'.format(len(app_classes), college_name + '.xlsx'))

if __name__ == '__main__':

    input_for_college()
