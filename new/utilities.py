# To do:
# Check for updates in search results page on UG
# Build new GUI (likely using tkinter, as I'm not that familiar with PyQt5)
# Build functions to search on UG and parse search results using updated Selenium
# Connect GUI and utility functions
import os,sys,json
import subprocess
import sys
from tqdm import tqdm
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
fail = False
try:
    from bs4 import BeautifulSoup as bs
except ImportError:
    fail = True
    print(f'WARNING: MODULE BeautifulSoup4 MISSING, ATTEMPTING TO INSTALL')
    install('beautifulsoup4')
from datetime import date, timedelta
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
except ImportError:
    fail = True
    print(f'WARNING: MODULE selenium MISSING, ATTEMPTING TO INSTALL')
    install('selenium')
from time import sleep
try:
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    fail = True
    print(f'WARNING: MODULE webdriver-manager MISSING, ATTEMPTING TO INSTALL')
    install('webdriver-manager')
try:
    import requests
except ImportError:
    fail = True
    print(f'WARNING: MODULE requests MISSING, ATTEMPTING TO INSTALL')
    install('requests')
if fail == True:
    print(f'WARNING: ONE OR MORE MODULES WERE MISSING AND HAVE BEEN INSTALLED. THE PROGRAM WILL NEED TO BE RE-RUN AS A RESULT.')
    quit()
# set up currentdir variable
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
# creating a simple logger
logger = open(os.path.join(currentdir,'logfile.txt'),'w')
# create a webdriver instance using selenium, set chrome options to headless to avoid a window popping up every time you scrape
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
# set chrome options "headless" to ensure a window doesn't pop up
chrome_options.add_argument("--headless")
# and the below line to simulate an actual browser window size
chrome_options.add_argument("--window-size=1100,1000")
# the below line instantiates the driver instance, with a simple webdriver check
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
# the below line gives us a useragent header to pretend to be a real browser
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})



SEARCH_URL = "https://www.ultimate-guitar.com/search.php?search_type=title&value={}"
RESULTS_PATTERN = "\&quot\;results\&quot\;:(\[.*?\]),\&quot\;pagination\&quot\;"
#RESULTS_PATTERN = "\"results\":(\[.*?\]),\"pagination\""
RESULTS_COUNT_PATTERN = "\&quot\;tabs\&quot\;,\&quot\;results_count\&quot\;:([0-9]+?),\&quot\;results\&quot\;"
#RESULTS_COUNT_PATTERN = "\"tabs\",\"results_count\":([0-9]+?),\"results\""
DOWNLOAD_TIMEOUT = 15
# retrieves a URL and returns a soup object
def retrieve(url):
    # retrieve the page using our driver instance
    driver.get(url)
    # sleep for 3 seconds to allow the page to fully load, and also to simulate human behavior
    sleep(3)
    # get the page source to scrape through for information
    data = driver.page_source
    # turn it into a soup object and return it
    soup = bs(data, features="html.parser")
    return soup

driver.close()