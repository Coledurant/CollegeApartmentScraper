# CollegeApartmentScraper

CollegeApartmentScraper is used to search for apartment complexes around college
campuses by using apartments.com.

Currently is set so only return apartment complexes that list 'Wi-Fi' in the
Features section of their webpage. This will be changed soon.

## Usage

Use the command line to search for apartments around a single college:

```bash
python CLIFinder.py
```

Required inputs:
  - College name
  - Enrollment
  - College location (city)
  - College state abbreviation

Optional (suggested to speed up, and increase accuracy of search) Inputs:
  - Address
  - Latitude
  - Longitude

This will save a CSV file to the CSVs folder along with an excel file to the
respective state abbreviation folder in the /Excels folder.
