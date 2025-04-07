# 07-Selenium module - Tab Switching

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

# 3. Open the first tab
driver.get("http://www.baidu.com")
time.sleep(1)

# 4. Set the search input
driver.find_element(By.ID, "kw").send_keys("python")
time.sleep(1)

# 5. Click the search button
driver.find_element(By.ID, 'su').click()
time.sleep(1)

# 6. Open a new tab by executing JavaScript code
js = "window.open('https://www.baidu.com')"
driver.execute_script(js)

# 7. Tab switching
# 7.1 Get all current browser window handles (tabs) as a list
windows = driver.window_handles

# 7.2 Switch to the first tab (Baidu)
driver.switch_to.window(windows[0])
time.sleep(2)

# 7.3 Switch to the second tab
driver.switch_to.window(windows[1])

# 8. Close the browser
time.sleep(6)
driver.quit()
