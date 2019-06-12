import os
import re
import sys
import json
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.common.exceptions import NoSuchElementException
from configparser import ConfigParser


SEARCH_URL = "https://www.ultimate-guitar.com/search.php?page={}&search_type=title&value={}"
RESULTS_PATTERN = "\"results\":(\[.*?\]),\"pagination\""
RESULTS_COUNT_PATTERN = "\"tabs\",\"results_count\":([0-9]+?),\"results\""
DOWNLOAD_TIMEOUT = 15


def search_tabs(search_string, types):
    page = 1
    # get first page of results
    response = requests.get(SEARCH_URL.format(page, search_string))
    # count is the number of results, used to know how many pages to search
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
                    ret.append((item["type"], item["artist_name"], item["song_name"],
                                str(round(float(item["rating"]), 1)), str(item["votes"]),
                                item["tab_url"], str(item["version"])))
            except KeyError:
                # key error on "official" tabs, not interested in these tabs
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


def download_tab(url, tab_type, artist, title, version):
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the pyInstaller bootloader
        # extends the sys module by a flag frozen=True
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(os.path.splitext(__file__)[0]))
    settings_file = os.path.join(application_path, "settings.cfg")

    config = ConfigParser()
    config.read(settings_file)
    cfg = config['MAIN']

    # get path to gecko executable by joining the application path with 'geckodriver' and the .exe file extension
    # if the executed tab_scraper is an exe
    gecko_path = (os.path.join(application_path, "geckodriver",
                               ".exe" if os.path.splitext(__file__)[1] == ".exe" else ""))[:-1]

    # create destination directory if it doesn't exist
    destination_root = cfg['destination_root']
    destination = os.path.join(destination_root, tab_type, artist)
    os.makedirs(destination, exist_ok=True)

    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options, executable_path=gecko_path)
    driver.get(url)

    # clear the privacy policy message
    try:
        popup_btn = driver.find_element_by_xpath('//button[text()="Got it, thanks!"]')
        popup_btn.click()
    except NoSuchElementException:
        pass

    # clear the official tab ad
    try:
        popup_btn = driver.find_element_by_xpath('//div[contains(@class, "ai-ah")]//button')
        popup_btn.click()
    except NoSuchElementException:
        pass

    # hide the autoscroll tool
    try:
        autoscroll = driver.find_element_by_xpath('//span[text()="Autoscroll"]/parent::button/parent::div/parent::section')
        driver.execute_script("arguments[0].setAttribute('style', 'display: none')", autoscroll)
    except NoSuchElementException:
        pass

    tab = driver.find_element_by_tag_name("pre")
    filename = os.path.join(destination, (title + " (Ver " + version + ")" + ".png"))
    tab.screenshot(filename)

    driver.quit()


def download_file(url, tab_type, artist):
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the pyInstaller bootloader
        # extends the sys module by a flag frozen=True
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(os.path.splitext(__file__)[0]))
    settings_file = os.path.join(application_path, "settings.cfg")
    config = ConfigParser()
    config.read(settings_file)
    cfg = config['MAIN']

    # get path to gecko executable by joining the application path with 'geckodriver' and the .exe file extension
    # if the executed tab_scraper is an exe
    gecko_path = (os.path.join(application_path, "geckodriver",
                               ".exe" if os.path.splitext(__file__)[1] == ".exe" else ""))[:-1]

    # create destination directory if it doesn't exist
    destination_root = cfg['destination_root']
    destination = os.path.join(destination_root, tab_type, artist)
    os.makedirs(destination, exist_ok=True)

    # count how many files are in the destination already
    nFiles = len(os.listdir(destination))

    options = Options()
    options.headless = True

    profile = FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", destination)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

    driver = webdriver.Firefox(options=options, firefox_profile=profile, executable_path=gecko_path)
    driver.get(url)
    button = driver.find_element_by_xpath('//button/span[text()="DOWNLOAD Guitar Pro TAB" '
                                          'or text()="DOWNLOAD Power TAB"]')
    driver.execute_script("arguments[0].click();", button)

    # kill firefox process after download completes or a timeout is reached
    downloading = True
    timeout = DOWNLOAD_TIMEOUT
    while downloading and timeout > 0:
        sleep(0.5)
        if len(os.listdir(destination)) > nFiles:
            downloading = False
        timeout -= 0.5
    driver.quit()
