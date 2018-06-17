"""
Adapted from:
https://medium.com/the-andela-way/introduction-to-web-scraping-using-selenium-7ec377a8cf72


Remaining Items:
----------------
TODO: Possibly revise recusion to not keep all solutions in memory at once.
Also, write solutions as they are generated rather than at the end. Also maybe 
use an actual generator.
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
###
import ipdb


def sleep_random(mini, maxi):
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
		sleep_random(0.25, 1.0)
		element = driver.find_element(*self.locator)
		return element.is_enabled()


def get_combos(browser, selects, out_path=None, verbose=False):
	"""
	: Recursive method to generate combinations from a series of select bars.
	"""

	if out_path:
		out_file = open(out_path, 'w')
	solutions = [] 
	
	def add_solution(solution):
		if verbose:
			print(solution)
		if out_path:
			out_file.write(json.dumps(solution, indent=2) + ',')
		solutions.append(solution)

	def get_combos_helper(index, prefix):
		if index > len(selects) - 1:
			add_solution(prefix)
			return
		xpath = selects[index][1]
		select_element = browser.find_element_by_xpath(xpath)
		select = Select(select_element)
		# Get all valid options. Exclude first value (filler) and any "--" entries.
		options = list(filter(lambda opt: opt.text != "--", select.options[1:]))
		if len(options) == 0:
			add_solution(prefix)
			return
		for option in options:
			select.select_by_visible_text(option.text)
			wait.until(element_is_enabled((By.XPATH, xpath)))
			new_prefix = copy.deepcopy(prefix)
			# Add entry for this selects attribute keyed to value. Ex. d['year'] = '1984'
			new_prefix[selects[index][0]] = option.text
			get_combos_helper(index + 1, new_prefix)
	get_combos_helper(0, {})

	if out_path:
		### Change later
		with open('motorcycles_.json', 'w') as out_file_:
			json.dump(out_file_, solutions, indent=2)
	
	try:
		out_file.close()
	except:
		pass
	return solutions

	


if __name__ == "__main__":
	
	# Define browser options
	option = chrome.webdriver.Options()
	option.add_argument("— incognito")

	# Instantiate browser
	browser = chrome.webdriver.WebDriver(
		executable_path = "C:/users/cjacoby/chromedriver/chromedriver.exe",
		chrome_options = option)

	# Setup browser wait mechanism, with 20 second timeout limit
	timeout = 20
	wait = WebDriverWait(browser, timeout)

	# Get page and check load success
	browser.get("https://www.ebay.com/b/Auto-Parts-and-Vehicles/6000/bn_1865334")

	# Test if the page loaded
	try:
		wait.until(
			EC.visibility_of_element_located(
				(By.XPATH, "//html")
			)
		)
	except TimeoutException:
		print("Timed out waiting for initial page load")
		browser.quit()
		sys.exit(1)

	# Click the button for motorcycles tab
	motorcycles_tab = browser.find_element_by_id("w5-w0-0-MOTORCYCLE-tab")
	motorcycles_tab.click()

	# Data structure fed to recursion
	select_container_xpath = '//form[@id="w5-w0-MOTORCYCLE-tabpanel"]/section/div'
	selects = [
		('year', select_container_xpath + "/span[1]/select"),
		('make', select_container_xpath + "/span[2]/select"),
		('model',  select_container_xpath + "/span[3]/select"),
		('trim', select_container_xpath + "/span[4]/select")
	]

	# Wait until first select bar is enabled to start main recursion process
	wait.until(element_is_enabled((By.XPATH, selects[0][1])))

	# main recursion process
	get_combos(browser, selects, out_path='motorcycles.json' ,verbose=True)