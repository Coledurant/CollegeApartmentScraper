from CollegeApps import *
from scraper import *

def input_for_college():

    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

    college_name = input('College Name (required): ')
    enrollment = int(input('Enrollment (required): '))
    college_location = input('City (required): ')
    state = input('State abbreviation (required): ').lower()

    while state.upper() not in states:

        state = input('State abbreviation (required): ').lower()

    address = input('Address: ')
    lat = float(input('Latitude of the point on campus you want to search around: '))
    lon = float(input('Longitude of the point on campus you want to search around: '))

    print('\n\nGetting apartments for {0}\n\n----------\n\n'.format(college_name))

    college = College(college_name=college_name, enrollment=enrollment, college_location=college_location, state=state, address=address, lat=lat, lon=lon)

    app_classes = college.find_apartments()

    print('{0} apartment complexes saved to an excel file at Excels/{1}'.format(len(app_classes), college_name + '.xlsx'))

if __name__ == '__main__':

    input_for_college()
