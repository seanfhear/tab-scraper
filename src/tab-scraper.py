import requests
import re
import json
import sys
# noinspection PyUnresolvedReferences
from PyQt5 import QtGui

# TODO pagination

SEARCH_URL = "https://www.ultimate-guitar.com/search.php?search_type=title&value={}"
RESULTS_PATTERN = "\"results\":(\[.*?\]),\"pagination\""

# define which types of tabs you're interested in getting
DESIRED_TYPES = ["Chords", "Tabs", "Pro"]

search_parameter = "%20".join(input("Enter search: ").split())
response = requests.get(SEARCH_URL.format(search_parameter))

try:
    # isolate results from page using regex
    results = re.search(RESULTS_PATTERN, response.content.decode()).group(1)
except AttributeError:
    results = ''
response_data = json.loads(results)

for item in response_data:
    try:
        # Get every result that has a desired type defined above
        if item["type"] in DESIRED_TYPES:
            print("Type: {}".format(item["type"]))
            print("Artist: {}".format(item["artist_name"]))
            print("Name: {}".format(item["song_name"]))
            print("{} Rating from {} Votes".format(round(float(item["rating"]), 2), item["votes"]))
            print(item["tab_url"])
            print()
    except KeyError:
        # key error on "official" tabs which have 'marketing_type' instead of 'type', not interested in these tabs
        ''
