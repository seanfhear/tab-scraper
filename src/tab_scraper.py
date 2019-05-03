import requests
import re
import json
import sys
# noinspection PyUnresolvedReferences
from PyQt5 import QtGui

# TODO pagination
# TODO remove warning suppressions

SEARCH_URL = "https://www.ultimate-guitar.com/search.php?search_type=title&value={}"
RESULTS_PATTERN = "\"results\":(\[.*?\]),\"pagination\""


def search_tabs(search_string, types):
    response = requests.get(SEARCH_URL.format(search_string))
    try:
        # isolate results from page using regex
        results = re.search(RESULTS_PATTERN, response.content.decode()).group(1)
    except AttributeError:
        results = ''
    response_data = json.loads(results)
    ret = []

    for item in response_data:
        try:
            # Get every result that has a desired type defined above
            if item["type"] in types:
                ret.append((item["type"], item["artist_name"], item["song_name"], str(round(float(item["rating"]), 2)),
                            str(item["votes"])))
                print("Type: {}".format(item["type"]))
                print("Artist: {}".format(item["artist_name"]))
                print("Name: {}".format(item["song_name"]))
                print("{} Rating from {} Votes".format(str(round(float(item["rating"]), 2)), item["votes"]))
                print(item["tab_url"])
                print()
        except KeyError:
            # key error on "official" tabs which have 'marketing_type' instead of 'type', not interested in these tabs
            ''
    return ret
