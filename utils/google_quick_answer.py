import requests
from bs4 import BeautifulSoup
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

handler = logging.FileHandler('CollegeApartmentScraper.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

def fetch_results(search_term, language_code):
    assert isinstance(search_term, str), 'Search term must be a string'
    escaped_search_term = search_term.replace(' ', '+')

    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, 1, language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()

    return search_term, response.text


def parse_results_for_quick_answer(html, search_term):

    LOGGER.info('searching for: {0}'.format(search_term))

    soup = BeautifulSoup(html, 'html.parser')

    result_block = soup.find('div', attrs={'class': 'Z0LcW'})

    if result_block == None:
        quick_answer = None

        LOGGER.debug('Quick answer scrape DID NOT WORK')
    else:
        quick_answer = result_block.text

        LOGGER.debug('Quick answer scrape WORKED')

    return quick_answer




def scrape_google_for_quick_answer(search_term, language_code="en"):
    try:
        question, html = fetch_results(search_term, language_code)
        results = parse_results_for_quick_answer(html, question)
        return results
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Google")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")

if __name__ == '__main__':

    try:
        results = scrape_google_for_quick_answer('University of Cincinnati Address')
        print(results)
    except Exception as e:
        print(e)
