# 04 - Requests module - Handling Cookies

import requests

# 1. Open the URL
response = requests.get("https://www.jd.com")

# 2. Get the cookie object from the response
cookie_obj = response.cookies

# 3. Output the cookie object
print("Cookie Object:", cookie_obj)

# 4. Convert the cookie object to a dictionary
cookie_dict = requests.utils.dict_from_cookiejar(cookie_obj)
print("Cookie Dictionary:", cookie_dict)
