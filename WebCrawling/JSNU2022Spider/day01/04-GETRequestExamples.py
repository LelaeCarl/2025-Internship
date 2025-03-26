"""
04-Requests Module - GET Request Example
"""

import requests

# 1. Basic GET request
# response = requests.get("https://www.baidu.com")
# print(response)

# response = requests.request("get", "https://www.baidu.com")
# print(response)

# 2. Adding headers and query parameters

# 2.1 Set the target URL
url = "https://www.baidu.com/s?"

# 2.2 Set user-agent header
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 2.3 Set query parameters
params = {
    "wd": "Great Wall"
}

# 2.4 Send the GET request using the requests module
response = requests.get(url=url, headers=headers, params=params)

# 2.5 Set the encoding for the response object
response.encoding = "utf-8"

# 2.6 Extract the response text data
html = response.text

# 2.7 Print the HTML content
print(html)

# 2.8 Print the type of the HTML content
print(type(html))

# 2.9 Print the text content as Unicode
print(response.text)

# 2.10 Print the raw content (bytes)
print(response.content)

# 2.11 Print the raw content again (for comparison)
print(response.content)

# 2.12 Print the HTTP status code of the response
print(response.status_code)

# 2.13 Print the final URL of the response
print(response.url)
