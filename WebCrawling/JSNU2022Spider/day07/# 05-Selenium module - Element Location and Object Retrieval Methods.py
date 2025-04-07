# 05-Selenium module - Element Location and Object Retrieval Methods
#     find_element(By.ID, '')                  -> Returns a single element node
#     find_element(By.CLASS_NAME, '')          -> Returns an element based on class name
#     find_element(By.NAME, '')                -> Returns an element based on the tag’s name attribute
#     find_element(By.XPATH, '')               -> Returns an element using an XPath expression
#     find_element(By.PARTIAL_LINK_TEXT, '')   -> Returns an element with partial link text
#     find_element(By.TAG_NAME, '')            -> Returns an element based on tag name
#     find_element(By.LINK_TEXT, '')           -> Returns an element with exact link text
#     find_element(By.CSS_SELECTOR, '')        -> Returns an element using a CSS selector
# Notes:
#     1. Difference between find_element and find_elements:
#         * With 's' returns a list; without 's' returns the first matching element
#         * find_element raises an exception if no match is found
#         * find_elements returns an empty list if no match is found
#     2. Difference between LINK_TEXT and PARTIAL_LINK_TEXT:
#         * LINK_TEXT requires exact text match; PARTIAL_LINK_TEXT matches if the text is contained

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By

# 1. Set the service object (automatically detect the version of the Chrome browser)
service = Service(
    executable_path=ChromeDriverManager().install()
)

# 2. Get the driver object
driver = webdriver.Chrome(service=service)

# 3. Send request to URL
driver.get("http://www.xbqg88.net/243_243094/2.html")

# 4.1 Return a single element by ID
print(driver.find_element(By.ID, 'play'))

# 4.2 Get an element by class name
print(driver.find_element(By.CLASS_NAME, 'con_top'))

# 4.3 Get an element by the 'name' attribute
print(driver.find_element(By.NAME, 'keywords'))

# 4.4 Get an element using XPath syntax
print(driver.find_element(By.XPATH, '//h1'))

# 4.5 Get an element by full link text
print(driver.find_element(By.LINK_TEXT, '下一页'))

# 4.6 Get an element by partial link text
print(driver.find_element(By.PARTIAL_LINK_TEXT, '章'))

# 4.7 Get an element by tag name
print(driver.find_element(By.TAG_NAME, 'a'))

# 4.8 Get an element using CSS selector
print(driver.find_element(By.CSS_SELECTOR, 'div#content'))

# Exit the browser
driver.quit()
