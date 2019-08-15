# CollegeApartmentScraper

CollegeApartmentScraper is used to search for apartment complexes around college
campuses by using apartments.com.

Currently is set so only return apartment complexes that list 'Wi-Fi' in the
Features section of their webpage. This will be changed soon.

## Installation

```bash
git clone https://github.com/Coledurant/CollegeApartmentScraper.git

cd CollegeApartmentScraper
```

Create virtualenv

```bash
virtualenv env
```

Activate virtualenv

Mac OS / Linux

```bash
source env/bin/activate
```
Windows

```bash
env\Scripts\activate
```

Install requirements

```bash
pip install -r requirements.txt
```

## Config

Edit the config.txt file inside of /conf by replacing {your_api_key_here} with
your Google Places API key, and changing the filename from config.txt to config.ini

  - If you do not have a key, one can be found here:
      https://developers.google.com/places/web-service/get-api-key
  - If there is no API present, or there is an error with the Google Places API,
    it will attempt to just scrape google quick answer for the address and latitude
    and longitude

## Usage

Use the command line to search for apartments around a single college:

```bash
python CLIFinder.py
```

Required inputs:
  - College name
  - College location (city)
  - College state abbreviation

Optional (just press enter if not answering) Inputs:
  - Address
  - Latitude
  - Longitude
  - Enrollment

This will save a CSV file to the CSVs folder along with an excel file to the
respective state abbreviation folder in the /Excels folder.
