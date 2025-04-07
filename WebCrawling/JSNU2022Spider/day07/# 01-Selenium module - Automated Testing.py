# 01-Selenium module - Automated Testing

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

# 4. Save a screenshot of the webpage as an image
driver.save_screenshot("baidu.png")

# 5. Output the title tag of the webpage
print(driver.title)

# 6. Close the Chrome browser
driver.quit()
