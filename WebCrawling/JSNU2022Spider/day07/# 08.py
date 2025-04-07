import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Specify the path to chromedriver (choose either method)
CHROME_DRIVER_PATH = r"C:\Users\Administrator\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Method 1: Use the chromedriver from the specified path
try:
    service = Service(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    print(f"Using specified Chromedriver path: {CHROME_DRIVER_PATH}")
except Exception as e:
    print(f"Failed to load custom path: {e}, attempting auto-download...")
    # Method 2: Automatically download a compatible chromedriver (backup plan)
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    print("Using auto-downloaded Chromedriver")

# Your original code continues here...
driver.get("http://wx.mail.qq.com/")
time.sleep(2)

try:
    # Switch to the outer login frame
    login_frame = driver.find_element(By.CLASS_NAME, "QQMailSdkTool_login_loginBox_qq_iframe")
    driver.switch_to.frame(login_frame)
    time.sleep(2)

    # Switch to the nested login iframe
    login_frame2 = driver.find_element(By.ID, "ptlogin_iframe")
    driver.switch_to.frame(login_frame2)
    time.sleep(2)

    # Click the "Account Password Login" switcher
    driver.find_element(By.XPATH, "//*[@id='switcher_plogin']").click()
    time.sleep(2)

    # Enter email address
    driver.find_element(By.XPATH, "//*[@id='u']").send_keys("2660884633@qq.com")
    time.sleep(2)

    # Enter password
    driver.find_element(By.XPATH, "//*[@id='p']").send_keys("15141569zmqzyj")
    time.sleep(2)

    # Click the login button
    driver.find_element(By.XPATH, "//*[@id='login_button']").click()
    time.sleep(5)

    # Switch back to the main window
    driver.switch_to.default_content()

    # Attempt to retrieve user info (example)
    try:
        content = driver.find_element(By.CLASS_NAME, "useraddr").text  # Replace with actual class name if needed
        print("Logged in user:", content)
    except Exception as e:
        print("Failed to retrieve user info:", e)
        driver.save_screenshot("userinfo_error.png")

except Exception as e:
    print("Error during operation:", e)
    driver.save_screenshot("operation_error.png")
finally:
    time.sleep(5)
    driver.quit()
