from geopy.geocoders import Nominatim, base
import geopy
import geopy.distance as distance
import time
import pandas as pd
import operator
import logging
import os
import requests
import json

from definitions import *
from utils.scraper import *
from utils.read_config import initialize_config, get_variable
from utils.google_quick_answer import scrape_google_for_quick_answer


################################################################################
################################################################################
################################################################################


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

handler = logging.FileHandler('CollegeApartmentScraper.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)

config_file_path = os.path.join(CONF_DIR, 'config.ini')

CONF = initialize_config(config_file_path)
PLACES_API_KEY = get_variable(conf = CONF, config_variable = 'PLACES_API_KEY',
                                variable_type = 'str', config_section = 'google_places')

GEOLOCATOR = Nominatim(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')


if not os.path.exists(CSV_DIR):
    os.mkdir(CSV_DIR)

if not os.path.exists(EXCEL_DIR):
    os.mkdir(EXCEL_DIR)


################################################################################
################################################################################
################################################################################


class College(object):

    '''
    A College Location that will be able to find apartments with Wi-Fi nearby

    Parameters:

        Required:

            college_name (str): A string of the college name
            enrollment (int): Enrollment number
            college_location (str): City of the college
            state (str): Two letter state abbreviation (will be turned to lower case)

        Optional:

            address (str): Address if one can be found, if not call self.find_address_from_google()
                            and let the Google Places API find the address
            lat (float): Latitude of the college if it can be found, if not call self.find_lat_lon()
                            and let geopy Nominatim find the lat, lon pair and save them
            lon (float): Longitude of the college if it can be found, if not call self.find_lat_lon()
                            and let geopy Nominatim find the lat, lon pair and save them
    '''

    def __init__(self, college_name, enrollment, college_location, state, address=None, lat=None, lon=None):

        self.college_name = college_name
        self.enrollment = enrollment
        self.college_location = college_location
        self.state = state.lower()
        self.address = address
        self.lat = lat
        self.lon = lon

    def find_address_from_google(self, PLACES_API_KEY = PLACES_API_KEY):

        '''
        Uses googles places API to search for the addess by the name of the college
        and adds that address to the college class
        Parameters:
            PLACES_API_KEY (str): API key for places API
        Returns:
            adress (str): The address of the place searched
        '''

        LOGGER.info('Searching for address on {0}'.format(self.college_name))

        search_term = self.college_name.replace(' ', '%20')

        search_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={0}&inputtype=textquery&fields=formatted_address&key={1}'.format(search_term, PLACES_API_KEY)

        request = requests.get(search_url).text

        data = json.loads(request)

        if data['status'] == 'OK':

            formatted_address = data.get('candidates')[0].get('formatted_address')

            self.address = formatted_address

            LOGGER.debug('Google Places API found address: {0}'.format(formatted_address))

        elif data['status'] == 'OVER_QUERY_LIMIT':

            LOGGER.warning('Google places API over limit')

            google_scrape_result = scrape_google_for_quick_answer("{0}, {1}, {2} Address".format(self.college_name, self.college_location, self.state))

            if google_scrape_result is not None:

                self.address = google_scrape_result

                LOGGER.debug('Google quick answer scrape found address: {0}'.format(self.address))

        else:

            LOGGER.error('Check College.find_address_from_google()')



    def find_lat_lon(self):

        '''
        Finds lat,lon pair from address by using geopy Nominatim
        '''

        LOGGER.info('Searching for lat, lon pair on {0} using geolocator'.format(self.college_name))


        try:
            location = GEOLOCATOR.geocode(self.address, timeout=base.DEFAULT_SENTINEL)
            lat = location.latitude
            lon = location.longitude

            self.lat = lat
            self.lon = lon

            LOGGER.debug('geolocator found lat, lon pair: ({0}, {1})'.format(self.lat, self.lon))

        except Exception as e:

            LOGGER.debug('geolocator did not find lat, lon pair because of an error:')
            LOGGER.debug(e)
            LOGGER.info('Trying to get lat, lon pair by scraping google quick answer')

            lat_lon_quick_scrape = scrape_google_for_quick_answer("{0}, {1}, {2} latitude and longitude".format(self.college_name, self.college_location, self.state))

            lat_lon_possible_list = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", lat_lon_quick_scrape)

            if len(lat_lon_possible_list) == 2:

                self.lat = float(lat_lon_possible_list[0])
                self.lon = float(lat_lon_possible_list[1])

                LOGGER.debug('Google quick answer scrape found lat, lon pair of {0}, {1}'.format(self.lat, self.lon))

            else:

                LOGGER.warning('{0} still has no lat, lon pair after trying everything'.format(self.college_name))

        finally:
            time.sleep(1)

    def find_apartments(self):

        '''
        Uses scraper.py to find apartments around the college using its state, city (location), and name by
        running scraper.main() and and turning all apartment.com information into a csv and finally turning it
        into an Excel file

        Returns:
            app_classes (list): A list of apartment classes that the scraper could find around the college campus
        '''

        LOGGER.info('Finding apartments for {0}'.format(self.college_name))

        fname = self.college_name + '.csv'

        if self.lat == None or self.lon == None:

            if self.address == None:

                self.find_address_from_google()

            self.find_lat_lon()

        apartments_base_url = 'https://www.apartments.com/off-campus-housing'

        university_apartments_url = apartments_base_url + '/{0}/{1}/{2}'.format(self.state.lower().replace(' ', '-'), self.college_location.lower().replace(' ', '-'), self.college_name.lower().replace(' ', '-'))

        main(university_apartments_url, fname)

        LOGGER.info('CSV saved to /CSVs')

        apartment_frame = get_frame(fname)

        app_classes = []

        for inum, row in apartment_frame.iterrows():

            app_class = Apartment(apartment_name = row['Option Name'], college = self, num_units = row['Units'], address = row['Address'], contact = row['Contact'], dist_from_college = None, lat = None, lon = None)

            app_class.find_lat_lon()

            app_class.get_dist_from_college()

            app_classes.append(app_class)

        app_class_frame = pd.DataFrame(columns = ['Name', 'Units', 'Distance From {0}'.format(self.college_name), 'Address', 'Contact', 'Lat', 'Lon'])

        for app_class in app_classes:

            row_data = {'Name':app_class.apartment_name, 'Units':app_class.num_units, 'Distance From {0}'.format(self.college_name):app_class.dist_from_college,
                        'Address':app_class.address, 'Contact':app_class.contact, 'Lat':app_class.lat, 'Lon':app_class.lon}

            new_row = pd.DataFrame(row_data, columns = list(row_data.keys()), index = [app_class.apartment_name])

            app_class_frame = pd.concat([app_class_frame, new_row], axis=0, ignore_index=True)

        os.chdir(EXCEL_DIR)
        state_dir = os.path.join(EXCEL_DIR, self.state)
        if not os.path.exists(state_dir):
            os.mkdir(state_dir)
        os.chdir(state_dir)

        writer = pd.ExcelWriter(fname.replace('.csv', '.xlsx'))
        app_class_frame.to_excel(writer, 'Apartments')
        writer.save()
        LOGGER.info('Excel saved to /Excels/{0}'.format(self.state))

        os.chdir(ROOT_DIR)

        self.apartment_classes = app_classes

        LOGGER.info('Apartment scrape finished for {0}'.format(self.college_name))

        return app_classes

class Apartment(object):

    '''
    An Apartment Location and all its relevent information. This will most likely
    be instantiated within a college class function College.find_apartments()

    Parameters:

        Required:

            apartment_name (str): A string of the apartment name
            college (College): The College class object that this apartment is near
            num_units (int): The number of apartment units
            address (str): The address of the apartment unit
            developer (str): The developer of the apartment
            contact (str): The phone number of the apartment
            year_built (int): Year the apartment was built

        Optional:

            lat (float): Latitude of the apartment if it can be found, if not call self.find_lat_lon()
                            and let geopy Nominatim find the lat, lon pair and save them
            lon (float): Longitude of the apartment if it can be found, if not call self.find_lat_lon()
                            and let geopy Nominatim find the lat, lon pair and save them
            dist_from_college (float): Distance the apartment is away from the college it is associated with.
                                        Most likely will be None to begin with and self.get_dist_from_college()
                                        will be called to find the distance
    '''

    def __init__(self, apartment_name, college, num_units, address, contact, developer=None, year_built=None, dist_from_college=None, lat=None, lon=None):

        self.apartment_name = apartment_name
        self.college = college
        self.num_units = num_units
        self.address = address
        self.developer = developer
        self.contact = contact
        self.year_built = year_built
        self.dist_from_college = dist_from_college
        self.lat = lat
        self.lon = lon

    def __str__(self):

        '''
        Name: Test apartment
        Units: 200
        College: Test College
        Mile's From College: 1.02
        '''

        return "Name: {0}\nUnits: {1}\nCollege: {2}\nMile's From College: {3}".format(self.apartment_name, self.num_units, self.college.college_name, self.dist_from_college)

    def find_lat_lon(self):

        '''
        Finds lat,lon pair from address by using geopy Nominatim and set them as
        the self.lat and self.lon pair
        '''


        try:
            location = GEOLOCATOR.geocode(self.address, timeout=base.DEFAULT_SENTINEL)
            lat = location.latitude
            lon = location.longitude

            self.lat = lat
            self.lon = lon

        except Exception as e:

            print(e)
            print('Apartment lat lon error')

        finally:
            time.sleep(1)


    def get_dist_from_college(self):

        '''
        Finds the distance away from the college the apartment is assigned to
        Parameters:
            self
        Returns:
            miles_away (float): The distance in miles between the college and apartment complex
        '''
        if self.lat is None or self.lon is None:
            self.find_lat_lon()
        else:pass


        try:
            college_lat_lon_tup = (self.college.lat, self.college.lon)
            if self.college.lat == None or self.college.lon == None:
                raise ValueError('Apartment lat or lon is None')
            self_lat_lon_tup = (self.lat, self.lon)
            miles_away = round(distance.distance(college_lat_lon_tup, self_lat_lon_tup).miles, 2)

            if miles_away >= 20:

                miles_away = None

        except Exception as e:
            LOGGER.error('Error finding distance from college for apartment {0} with lat lon pair ({1}, {2}) and address {3}'.format(self.apartment_name, self.lat, self.lon, self.address))
            LOGGER.error(e)
            miles_away = None

        self.dist_from_college = miles_away

        return miles_away


################################################################################
################################################################################
################################################################################


if __name__ == '__main__':

    penn = College('University of Pennsylvania', 24806, 'Philadelphia', 'pa', '3401 Walnut St, Philadelphia, PA 19104', 39.952935, -75.194963)

    penn.find_apartments()
