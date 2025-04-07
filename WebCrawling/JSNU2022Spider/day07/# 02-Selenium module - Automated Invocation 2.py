# 02-Selenium module - Automated Invocation 2

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 1. Set the service object (automatically detect the version of the Chrome browser)
service = Service(
    executable_path=ChromeDriverManager().install()
)

# 2. Get the driver object
driver = webdriver.Chrome(service=service)

# 3. Send request to URL
driver.get("https://www.baidu.com/")

driver.quit()
