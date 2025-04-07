# 03-Selenium module - Click Event

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
driver.get("http://www.xbiqugu.la/modules/article/waps.php")

# 4. Set the content of the search box (by tag's ID value)
driver.find_element(By.ID, 'wd').send_keys("一念永恒")

# 5. Click the search button (by tag's ID value)
driver.find_element(By.ID, 'sss').click()

# 6. Set delay before closing
time.sleep(10)

# 7. Close the browser
driver.quit()
