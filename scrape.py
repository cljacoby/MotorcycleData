""" https://medium.com/the-andela-way/introduction-to-web-scraping-using-selenium-7ec377a8cf72 """


from selenium.webdriver import chrome
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from time import sleep
from random import random
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
		sleep_random(0.25, 0.75)
		element = driver.find_element(*self.locator)
		return element.is_enabled()


def write_selects(select, out_path, verbose):
	"""
	: Recursive method to get all combinations from an array-struct of select bars.
	"""

	# The output json file
	out_file = open(out_path, 'w')

	def write_selects_helper(index, prefix):
		if index > len(selects) - 1:
			# Exit 1: Out of range of attribute selectors
			return False
		label, select = selects[index]
		if not len(select.options) > 1:
			# Exit 2: No options. 0th option is a filler and doesn't count. 
			return False
		options = select.options[1:]
		wrote_once = False
		for opt in options:
			current = { label, opt.text }
			next_prefix = prefix[:]
			next_prefix.append(current)
			result = write_selects_helper(s_idnex + 1, next_prefix)
			wrote_once = wrote_once or result
		if not wrote_once:
			if verbose: print(prefix)
			json.dump(prefix)
		return True

	write_motorcycles_helper(0, [])
	out_file.close()


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

	# Set xpaths
	select_container_xpath = '//form[@id="w5-w0-MOTORCYCLE-tabpanel"]/section/div'
	year_select_xpath = select_container_xpath + "/span[1]/select"
	make_select_xpath = select_container_xpath + "/span[2]/select"
	model_select_xpath = select_container_xpath + "/span[3]/select"
	trim_select_xpath = select_container_xpath + "/span[4]/select"

	# Set the select bar container
	select_container = browser.find_element_by_xpath(select_container_xpath)
	
	# Set the WebElement instances of select bars
	year_element = select_container.find_element_by_xpath(year_select_xpath)
	make_element = select_container.find_element_by_xpath(make_select_xpath)
	model_element = select_container.find_element_by_xpath(model_select_xpath)
	trim_element = select_container.find_element_by_xpath(trim_select_xpath)

	# Set the Selenium UI select helper instances
	year_select = Select(year_element)
	make_select = Select(make_element)
	model_select = Select(model_element)
	trim_select = Select(trim_element)

	# Setup data structure that will help the main execution, which generates all permutation via recursion
	# Change instances to XPATHS and in recursion do the wait.until...
	selects = [
		('year', year_select),
		('make', make_select),
		('model', model_select),
		('trim', trim_select)
	]

	# Wait until first select bar is enabled before starting
	wait.until(element_is_enabled((By.XPATH, year_select_xpath)))


	with open("./motorcycles.json") as out_file:
		out_file.write('[')

		# Works, but could be more structured with recursion rather than stacked loops
		# Main loop. Get all combinations of select bars.
		for year in year_select.options[1:]:
			year_select.select_by_visible_text(year.text)
			wait.until(element_is_enabled((By.XPATH, year_select_xpath)))
			wrote_below = False
			for make in make_select.options[1:]:
				make_select.select_by_visible_text(make.text)
				wait.until(element_is_enabled((By.XPATH, make_select_xpath)))
				wrote_below = False
				for model in model_select.options[1:]:
					model_select.select_by_visible_text(model.text)
					wait.until(element_is_enabled((By.XPATH, model_select_xpath)))
					wrote_below = False
					for trim in trim_select.options[1:]:
						trim_select.select_by_visible_text(trim.text)
						wait.until(element_is_enabled((By.XPATH, trim_select_xpath)))
						print(year.text, make.text, model.text, trim.text)
					if not wrote_below:
						pass	