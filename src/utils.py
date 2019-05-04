import requests
import re
import json
# noinspection PyUnresolvedReferences
from PyQt5 import QtGui
from bs4 import BeautifulSoup

# TODO remove warning suppressions

SEARCH_URL = "https://www.ultimate-guitar.com/search.php?page={}&search_type=title&value={}"
RESULTS_PATTERN = "\"results\":(\[.*?\]),\"pagination\""
RESULTS_COUNT_PATTERN = "\"tabs\",\"results_count\":([0-9]+?),\"results\""


def search_tabs(search_string, types):
    page = 1
    # get first page of results
    response = requests.get(SEARCH_URL.format(page, search_string))
    count = 0
    try:
        # isolate results from page using regex
        response_body = response.content.decode()
        results = re.search(RESULTS_PATTERN, response_body).group(1)
        count = int(re.search(RESULTS_COUNT_PATTERN, response_body).group(1))
    except AttributeError:
        results = ''
    response_data = json.loads(results)
    ret = []

    while count > 0:
        for item in response_data:
            try:
                # Get every result that has a desired type
                if item["type"] in types:
                    ret.append((item["type"], item["artist_name"], item["song_name"], str(round(float(item["rating"]), 2)),
                                str(item["votes"]), item["tab_url"], str(item["version"])))
            except KeyError:
                # key error on "official" tabs which have 'marketing_type' instead of 'type', not interested in these tabs
                ''
            count -= 1
        if count > 0:
            page += 1
            response = requests.get(SEARCH_URL.format(page, search_string))
            try:
                # isolate results from page using regex
                response_body = response.content.decode()
                results = re.search(RESULTS_PATTERN, response_body).group(1)
            except AttributeError:
                results = ''
            response_data = json.loads(results)
    return ret


def download_tab(url):
    print("downloading tab...")


def download_file(url):
    print("downloading file...")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    print(soup)
    dl_form = soup.find('form')
    print(dl_form)
