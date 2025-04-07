# 06-Selenium module - Element Text and Attribute Values
#     element.click()            -> Perform click operation on an element
#     element.send_keys(data)    -> Input data into a text field
#     element.text               -> Get the text content of an element
#     element.get_attribute()    -> Get the value of a specified attribute of an element

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

# 4.1 Define and perform click operation on the first <a> tag
driver.find_element(By.TAG_NAME, 'a').click()

# 4.2 Locate the element with ID 'wd' and input '一念永恒' after clearing
driver.find_element(By.ID, 'wd').clear()
driver.find_element(By.ID, 'wd').send_keys("一念永恒")

# 4.3 Get the text content of an element object
data = driver.find_element(By.XPATH, "//h1")
print(data.text)

# 4.4 Get the attribute value of an element object
attrList = driver.find_elements(By.LINK_TEXT, "下一页")
print(attrList[0].get_attribute("href"))

# Quit the browser
driver.quit()
