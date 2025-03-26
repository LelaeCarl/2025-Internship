# 02 - Requests module - Using Proxy

import requests

# 1. Set the User-Agent headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# 2. Set up IP proxies
proxies = {
    "https": "117.42.94.129:23622",
    "http": "117.42.94.183:16272"
}

# 3. Send the request through the proxy
response = requests.get(
    url="https://www.baidu.com",
    headers=headers,
    proxies=proxies
)

# 4. Output the result
response.encoding = "utf-8"
print(response.text)
