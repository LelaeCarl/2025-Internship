# 05 - Requests Module - Using Session

import requests

# 1. Create a session object to store cookies
session = requests.session()

# 2. Set the request headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# 3. Set the login credentials (username and password)
data = {
    'email': 'sdujack999',
    'password': '*****'   # Replace '*****' with the actual password if needed
}

# 4. Send a POST request with login data
session.post("http://www.renren.com/PLogin.do", data=data, headers=headers)

# 5. Use the session (with the login cookies) to access a page that requires login
response = session.get(
    "https://www.renren.com/410003129/profile",
    headers=headers
)

# 6. Print the content of the response
print(response.text)
