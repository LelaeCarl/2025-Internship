# 04-Selenium module - Common Attributes and Methods
#     driver.page_source     -> Source code of the current tab after browser rendering
#     driver.current_url     -> URL of the current tab
#     driver.close()         -> Close the current tab; if it's the only one, closes the browser
#     driver.quit()          -> Quit the browser completely
#     driver.forward()       -> Navigate forward
#     driver.back()          -> Navigate back
#     driver.save_screenshot(img_name) -> Take a screenshot of the page

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
driver.get("http://www.baidu.com")

# 4. Get the rendered source code of the webpage
print(driver.page_source)

# 5. Get the URL of the current page
print(driver.current_url)

# 6. Quit the browser
driver.quit()
