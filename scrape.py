"""
Adapted from:
https://medium.com/the-andela-way/introduction-to-web-scraping-using-selenium-7ec377a8cf72


Remaining Items:
----------------
TODO: Handle website crash/disconnect errors. Basically. Get the last entry before
failure, then start bcack up after that.
TODO: Switch to databse intermediary rather than trying to write straight to a flat
file.
"""


from selenium.webdriver import chrome
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from time import sleep
from random import random
import copy
import json
import sqlite3
###
import ipdb


def sleep_rand_interval(mini, maxi):
	"""
	: Sleep for a random duraction on an interval. Arguments mini and maxi
	: are specified in seconds.
	"""
	duration = (maxi - mini) * random() + mini
	sleep(duration)


class element_is_enabled(object):
	"""
	: A custom Selenium wait condition that will wait until an element is enabled
	: (a.k.a. not having attr 'disabled') before continuing actions. The call method
	: encorporates a sleep_random execution.
	"""

	def __init__(self, locator):
		self.locator = locator

	def __call__(self, driver):
		sleep_rand_interval(.25, .25)
		element = driver.find_element(*self.locator)
		return element.is_enabled()


def get_valid_options(options, bad_values, start_val=None):
	"""
	: Get valid options from a selenium select instance's options list. Filters
	: out bad_values. Also cuts first element from every options list, which is always
	: a filler value. If start_val is passed, reduces options to those past the
	: start_val (not inclusiv). Useful for resuming a process that previously failed
	: intermittently.
	"""
	valid_options = []
	start = False if start_val else True
	for opt in options:
		if start and opt.text not in bad_values:
			valid_options.append(opt)
		if opt.text == start_val:
			start = True
	return valid_options



def get_combos(browser, selects_struct, index, prefix):
	"""
	: Generate all combinations of the select bars defined in selects_struct.
	: Operates via a recursive generator, so combos are delivered one at a time as
	: dictionaries.
	"""
	if index > len(selects_struct) - 1:
		yield prefix
		return
	# Construct selenium Select UI helper from the xpath
	xpath = selects_struct[index]['xpath']
	select_element = browser.find_element_by_xpath(xpath)
	select = Select(select_element)
	# Get all valid options. Exclude first value, which is a filler.
	start_val = selects_struct[index]['start'] if 'start' in selects_struct[index] else None  
	options = get_valid_options(select.options[1:], bad_values=['--'], start_val=start_val)
	if len(options) == 0:
		yield prefix
		return
	for option in options:
		select.select_by_visible_text(option.text)
		wait.until(element_is_enabled((By.XPATH, xpath)))
		new_prefix = copy.deepcopy(prefix)
		# Add entry for this selects_struct attribute, keyed to the value. Ex. d['year'] = '1984'
		new_prefix[selects_struct[index]['attr']] = option.text
		for combo in get_combos(browser, selects_struct, index + 1, new_prefix):
			yield combo


def setup_browser():
	# Define browser options
	option = chrome.webdriver.Options()
	option.add_argument("— incognito")

	# Instantiate browser
	browser = chrome.webdriver.WebDriver(
		executable_path = "C:/users/cjacoby/chromedriver/chromedriver.exe",
		chrome_options = option)

	# Setup browser wait instance, with timeout limit
	timeout = 20
	wait = WebDriverWait(browser, timeout)

	# Get page and check load success
	browser.get("https://www.ebay.com/b/Auto-Parts-and-Vehicles/6000/bn_1865334")

	# Test if the page loaded
	try:
		wait.until(EC.visibility_of_element_located((By.XPATH, "//html")))
		return browser, wait
	except TimeoutException:
		print("Timed out waiting for initial page load")
		browser.quit()
		sys.exit(1)




if __name__ == "__main__":

	# Get a prepared browser instance
	browser, wait = setup_browser()

	# Click the button for motorcycles tab
	motorcycles_tab = browser.find_element_by_id("w5-w0-0-MOTORCYCLE-tab")
	motorcycles_tab.click()

	# Select bar data structure fed to recursion
	select_container_xpath = '//form[@id="w5-w0-MOTORCYCLE-tabpanel"]/section/div'
	selects_struct = [
		{'attr': 'year', 'xpath': select_container_xpath + "/span[1]/select"},
		{'attr': 'make', 'xpath': select_container_xpath + "/span[2]/select"},
		{'attr': 'model', 'xpath':  select_container_xpath + "/span[3]/select"},
		{'attr': 'trim', 'xpath': select_container_xpath + "/span[4]/select"}
	]

	# Wait until first select bar is enabled to start main recursion process
	wait.until(element_is_enabled((By.XPATH, selects_struct[0]['xpath'])))

	# main process
	for combo in get_combos(browser, selects_struct, 0, {}):
		print(combo)