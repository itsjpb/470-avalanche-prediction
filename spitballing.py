"""
First off, this code is not great. The filename says it all.

This code utilizes selenium, a webscraping tool, to pull archived
avalanche danger reports. An alternative tool, BeautifulSoup, is 
NOT used because it only scrapes HTML data and not the JavaScript
data that the Northwest Avalanche Center (NWAC) site uses for 
display. Selenium is a bit of a beast to work with unfortunately
and if another tool is available we should at least look into it.

This code opens and navigates to the NWAC archived avalanche reports
site and pulls the links to individual avalanche reports. Then these
pages are scraped to find danger ratings.
"""

import os
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

def init_driver():
    """Initialize the web driver (essentially 'open the webpage')"""
    # `snap install firefox`
    # --- 
    # Set up the webdriver. 
    # This code will likely be different depending on the user's computer. 
    install_dir = "/snap/firefox/current/usr/lib/firefox"
    driver_loc = os.path.join(install_dir, "geckodriver")
    binary_loc = os.path.join(install_dir, "firefox")

    service = Service(driver_loc)
    opts = Options()
    opts.add_argument('-headless')
    opts.binary_location = binary_loc
    # ---
    driver = webdriver.Firefox(service=service, options=opts)
    return driver

def print_danger_ratings(url):
    # Make a new driver because reuse sometimes causes problems
    driver = init_driver()
    driver.get(url)
    time.sleep(2)
    # Find all elements with the specified class name
    res = driver.find_elements(By.CLASS_NAME, 'nac-dangerLabel')
    print('actual:')
    for danger in res:
        if danger.text:
            print('\t'+danger.text)

def test_danger_ratings(driver, url, expected):
    print('expected:')
    print(expected)
    print_danger_ratings(url)

driver = init_driver()

def run_some_tests():
    test_danger_ratings(driver, 'https://nwac.us/avalanche-forecast/#/forecast/6/124162', \
                        '\tmoderate\n\tmoderate\n\tlow')
    print('---')
    test_danger_ratings(driver, 'https://nwac.us/avalanche-forecast/#/forecast/4/124286',\
                        '\tconsiderable\n\tconsiderable\n\tmoderate')
    print('---')
    test_danger_ratings(driver, 'https://nwac.us/avalanche-forecast/#/forecast/4/123859',\
                        '\thigh\n\thigh\n\tconsiderable')
    print('---')
    test_danger_ratings(driver, 'https://nwac.us/avalanche-forecast/#/forecast/2/123737',\
                        '\tmoderate\n\tmoderate\n\tmoderate')
    print('---')

# run_some_tests()

# NWAC Archived Avalanche Reports from the 22-23 season
# Provides daily danger predictions by area
archive = 'https://nwac.us/avalanche-forecast/#/archive/'
# "Get" the page
driver.get(archive)
# Wait for the page to load. There's probably a much better way to do this
time.sleep(2)

# Get the link to the report page
# This is where selenium gets weird about navigating things...
# See documentation for more info, but it's finding it my XML path
page = driver.find_elements(By.XPATH, "//a[contains(@href, '#/forecast/')]")
for p in page[15:20]:
    print('link:', p.get_attribute('href'))
    print_danger_ratings(p.get_attribute('href'))

driver.close()
